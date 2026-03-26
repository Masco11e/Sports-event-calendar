from flask import Flask, jsonify, request, render_template, abort, send_from_directory
from database import get_connection, init_db, seed_db
import os

app= Flask(__name__, template_folder=".", static_folder="src", static_url_path="/src")

def rows_to_list(rows):
    return [dict(r) for r in rows]

@app.get("/api/matches")
def get_matches():
    competition= request.args.get("competition")
    date_from=   request.args.get("date_from")
    date_to=     request.args.get("date_to")
    status=      request.args.get("status")

    sql= """
        SELECT
            m.id, m.season, m.date_venue, m.time_venue_utc, m.status,
            m.stadium, m.description, m.home_stage_position, m.away_stage_position,
            c.id AS competition_id, c.name AS competition_name, c.slug AS competition_slug,
            s.id AS stage_id, s.name AS stage_name, s.ordering AS stage_ordering,
            ht.id AS home_team_id, ht.name AS home_team_name,
            ht.official_name AS home_team_official, ht.abbreviation AS home_team_abbr,
            ht.country_code AS home_team_country,
            at.id AS away_team_id, at.name AS away_team_name,
            at.official_name AS away_team_official, at.abbreviation AS away_team_abbr,
            at.country_code AS away_team_country,
            mr.home_goals, mr.away_goals, mr.message AS result_message,
            wt.name AS winner_name, wt.id AS winner_id
        FROM match m
        JOIN competition c ON m._competition_id= c.id
        JOIN stage s ON m._stage_id= s.id
        LEFT JOIN team ht ON m._home_team_id= ht.id
        LEFT JOIN team at ON m._away_team_id= at.id
        LEFT JOIN match_result mr ON mr._match_id= m.id
        LEFT JOIN team wt ON mr._winner_team_id= wt.id
        WHERE 1=1
    """
    params= []

    if competition:
        sql += " AND c.id= ?"
        params.append(competition)
    if date_from:
        sql += " AND m.date_venue >= ?"
        params.append(date_from)
    if date_to:
        sql += " AND m.date_venue <= ?"
        params.append(date_to)
    if status:
        sql += " AND m.status= ?"
        params.append(status)

    sql += " ORDER BY m.date_venue, m.time_venue_utc"

    conn= get_connection()
    rows= conn.execute(sql, params).fetchall()

    events_by_match= {}
    if rows:
        ids= [r["id"] for r in rows]
        ph= ",".join("?" * len(ids))
        events= conn.execute(f"""
            SELECT me.*, t.name AS team_name, t.abbreviation AS team_abbr
            FROM match_event me
            LEFT JOIN team t ON me._team_id= t.id
            WHERE me._match_id IN ({ph})
        """, ids).fetchall()
        for e in events:
            events_by_match.setdefault(e["_match_id"], []).append(dict(e))

    conn.close()

    result= []
    for r in rows:
        d= dict(r)
        d["events"]= events_by_match.get(d["id"], [])
        result.append(d)

    return jsonify(result)

@app.get("/api/matches/<int:match_id>")
def get_match(match_id):
    conn= get_connection()
    row= conn.execute("""
        SELECT
            m.*,
            c.name AS competition_name, c.slug AS competition_slug,
            s.name AS stage_name, s.ordering AS stage_ordering,
            ht.name AS home_team_name, ht.official_name AS home_team_official,
            ht.abbreviation AS home_team_abbr, ht.country_code AS home_team_country,
            at.name AS away_team_name, at.official_name AS away_team_official,
            at.abbreviation AS away_team_abbr, at.country_code AS away_team_country,
            mr.home_goals, mr.away_goals, mr.message AS result_message,
            wt.name AS winner_name
        FROM match m
        JOIN competition c ON m._competition_id= c.id
        JOIN stage s ON m._stage_id= s.id
        LEFT JOIN team ht ON m._home_team_id= ht.id
        LEFT JOIN team at ON m._away_team_id= at.id
        LEFT JOIN match_result mr ON mr._match_id= m.id
        LEFT JOIN team wt ON mr._winner_team_id= wt.id
        WHERE m.id= ?
    """, (match_id,)).fetchone()

    if not row:
        conn.close()
        abort(404)

    data= dict(row)

    result_row= conn.execute("SELECT id FROM match_result WHERE _match_id= ?", (match_id,)).fetchone()
    if result_row:
        periods= conn.execute("SELECT * FROM score_by_period WHERE _result_id= ?", (result_row["id"],)).fetchall()
        data["score_by_periods"]= rows_to_list(periods)
    else:
        data["score_by_periods"]= []

    events= conn.execute("""
        SELECT me.*, t.name AS team_name, t.abbreviation AS team_abbr
        FROM match_event me
        LEFT JOIN team t ON me._team_id= t.id
        WHERE me._match_id= ?
        ORDER BY me.minute
    """, (match_id,)).fetchall()
    data["events"]= rows_to_list(events)

    conn.close()
    return jsonify(data)

@app.post("/api/matches")
def create_match():
    body= request.get_json(force=True)

    for field in ["_stage_id", "season", "date_venue", "status"]:
        if not body.get(field):
            return jsonify({"error": f"Missing required field: {field}"}), 400

    competition_name= body.get("competition_name", "").strip()
    if not competition_name:
        return jsonify({"error": "Missing required field: competition_name"}), 400

    conn= get_connection()
    cur=  conn.cursor()

    existing= cur.execute("SELECT id FROM competition WHERE name= ?", (competition_name,)).fetchone()
    if existing:
        competition_id= existing["id"]
    else:
        count= cur.execute("SELECT COUNT(*) AS c FROM competition").fetchone()["c"]
        competition_id= f"competition-{count + 1}"
        cur.execute("INSERT INTO competition (id, slug, name) VALUES (?, ?, ?)",
            (competition_id, competition_id, competition_name))

    if not cur.execute("SELECT id FROM stage WHERE id= ?", (body["_stage_id"],)).fetchone():
        cur.execute("INSERT INTO stage (id, _competition_id, name, ordering) VALUES (?, ?, ?, ?)",
            (body["_stage_id"], competition_id, body.get("stage_name", body["_stage_id"]), body.get("stage_ordering", 1)))

    for key in ("home_team", "away_team"):
        team= body.get(key)
        if team and team.get("slug"):
            cur.execute("INSERT OR IGNORE INTO team (id, name, official_name, slug, abbreviation, country_code) VALUES (?, ?, ?, ?, ?, ?)",
                (team["slug"], team.get("name", ""), team.get("official_name", ""),
                 team["slug"], team.get("abbreviation", ""), team.get("country_code", "")))

    home_id= body.get("home_team", {}).get("slug") if body.get("home_team") else None
    away_id= body.get("away_team", {}).get("slug") if body.get("away_team") else None

    cur.execute("""
        INSERT INTO match (_competition_id, _stage_id, _group_id, _home_team_id, _away_team_id,
            season, date_venue, time_venue_utc, status, stadium, description)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (competition_id, body["_stage_id"], body.get("_group_id"),
          home_id, away_id, body["season"], body["date_venue"],
          body.get("time_venue_utc", "00:00:00"), body["status"],
          body.get("stadium"), body.get("description")))
    match_id= cur.lastrowid

    result= body.get("result")
    if result:
        winner_id= (result.get("winner_id") or
            (away_id if result.get("winner") == body.get("away_team", {}).get("name") else
             home_id if result.get("winner") else None))
        cur.execute("INSERT INTO match_result (_match_id, home_goals, away_goals, _winner_team_id, message) VALUES (?, ?, ?, ?, ?)",
            (match_id, result.get("home_goals", 0), result.get("away_goals", 0), winner_id, result.get("message")))

    conn.commit()
    conn.close()
    return jsonify({"id": match_id, "message": "Match created successfully"}), 201

@app.get("/api/competitions")
def get_competitions():
    conn= get_connection()
    rows= conn.execute("SELECT * FROM competition ORDER BY name").fetchall()
    conn.close()
    return jsonify(rows_to_list(rows))

@app.get("/api/stages")
def get_stages():
    conn= get_connection()
    rows= conn.execute("SELECT * FROM stage ORDER BY ordering").fetchall()
    conn.close()
    return jsonify(rows_to_list(rows))

@app.post("/api/import")
def import_matches():
    data= request.get_json(force=True)
    if not data or "data" not in data:
        return jsonify({"error": "Missing 'data' key"}), 400

    conn= get_connection()
    cur=  conn.cursor()
    imported= 0

    for item in data["data"]:
        competition_id=   item.get("originCompetitionId")
        competition_name= item.get("originCompetitionName", competition_id)
        if not competition_id:
            continue

        if not cur.execute("SELECT id FROM competition WHERE id= ?", (competition_id,)).fetchone():
            cur.execute("INSERT INTO competition (id, slug, name) VALUES (?, ?, ?)",
                (competition_id, competition_id, competition_name))

        stage=    item.get("stage", {})
        stage_id= stage.get("id")
        if stage_id and not cur.execute("SELECT id FROM stage WHERE id= ?", (stage_id,)).fetchone():
            cur.execute("INSERT INTO stage (id, _competition_id, name, ordering) VALUES (?, ?, ?, ?)",
                (stage_id, competition_id, stage.get("name", stage_id), stage.get("ordering", 1)))

        for key in ("homeTeam", "awayTeam"):
            team= item.get(key)
            if team and team.get("slug"):
                cur.execute("INSERT OR IGNORE INTO team (id, name, official_name, slug, abbreviation, country_code) VALUES (?,?,?,?,?,?)",
                    (team["slug"], team.get("name",""), team.get("officialName",""),
                     team["slug"], team.get("abbreviation",""), team.get("teamCountryCode","")))

        home_id= item.get("homeTeam",{}).get("slug") if item.get("homeTeam") else None
        away_id= item.get("awayTeam",{}).get("slug") if item.get("awayTeam") else None

        cur.execute("""
            INSERT INTO match (_competition_id,_stage_id,_group_id,_home_team_id,_away_team_id,
                season,date_venue,time_venue_utc,status,stadium)
            VALUES (?,?,?,?,?,?,?,?,?,?)""", 
            (competition_id, stage_id, None, home_id, away_id,
              item.get("season"), item.get("dateVenue"),
              item.get("timeVenueUTC","00:00:00"), item.get("status","scheduled"),
              item.get("stadium")))
        match_id= cur.lastrowid

        result= item.get("result")
        if result and item.get("status") == "played":
            winner_name= result.get("winner")
            winner_id= (away_id if winner_name == item.get("awayTeam",{}).get("name") else
                        home_id if winner_name == item.get("homeTeam",{}).get("name") else None)
            cur.execute("INSERT OR IGNORE INTO match_result (_match_id,home_goals,away_goals,_winner_team_id,message) VALUES (?,?,?,?,?)",
                (match_id, result.get("homeGoals",0), result.get("awayGoals",0), winner_id, result.get("message")))

        imported += 1

    conn.commit()
    conn.close()
    return jsonify({"imported": imported}), 201

@app.get("/api/export")
def export_matches():
    conn= get_connection()
    rows= conn.execute("""
        SELECT
            m.season, m.status, m.time_venue_utc AS timeVenueUTC,
            m.date_venue AS dateVenue, m.stadium,
            ht.name AS home_name, ht.official_name AS home_official,
            ht.slug AS home_slug, ht.abbreviation AS home_abbr, ht.country_code AS home_country,
            at.name AS away_name, at.official_name AS away_official,
            at.slug AS away_slug, at.abbreviation AS away_abbr, at.country_code AS away_country,
            mr.home_goals, mr.away_goals, wt.name AS winner,
            s.id AS stage_id, s.name AS stage_name, s.ordering AS stage_ordering,
            c.id AS competition_id, c.name AS competition_name
        FROM match m
        JOIN competition c ON m._competition_id= c.id
        JOIN stage s ON m._stage_id= s.id
        LEFT JOIN team ht ON m._home_team_id= ht.id
        LEFT JOIN team at ON m._away_team_id= at.id
        LEFT JOIN match_result mr ON mr._match_id= m.id
        LEFT JOIN team wt ON mr._winner_team_id= wt.id
        ORDER BY m.date_venue, m.time_venue_utc
    """).fetchall()
    conn.close()

    data= []
    for r in rows:
        data.append({
            "season":    r["season"],
            "status":    r["status"],
            "timeVenueUTC": r["timeVenueUTC"],
            "dateVenue": r["dateVenue"],
            "stadium":   r["stadium"],
            "homeTeam": {"name": r["home_name"], "officialName": r["home_official"],
                         "slug": r["home_slug"], "abbreviation": r["home_abbr"],
                         "teamCountryCode": r["home_country"]} if r["home_slug"] else None,
            "awayTeam": {"name": r["away_name"], "officialName": r["away_official"],
                         "slug": r["away_slug"], "abbreviation": r["away_abbr"],
                         "teamCountryCode": r["away_country"]} if r["away_slug"] else None,
            "result": {"homeGoals": r["home_goals"], "awayGoals": r["away_goals"],
                       "winner": r["winner"]} if r["home_goals"] is not None else None,
            "stage": {"id": r["stage_id"], "name": r["stage_name"], "ordering": r["stage_ordering"]},
            "originCompetitionId":   r["competition_id"],
            "originCompetitionName": r["competition_name"],
        })

    return jsonify({"data": data})

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/pages/teams.html")
def teams():
    return send_from_directory(os.path.join(os.path.dirname(__file__), "pages"), "teams.html")

@app.get("/pages/stats.html")
def stats():
    return send_from_directory(os.path.join(os.path.dirname(__file__), "pages"), "stats.html")

@app.get("/public/images/<path:filename>")
def public_images(filename):
    return send_from_directory(os.path.join(os.path.dirname(__file__), "public", "images"), filename)

if __name__== "__main__":
    if not os.path.exists(os.path.join(os.path.dirname(__file__), "sports.db")):
        init_db()
        seed_db()
    app.run(debug=True, port=8080)