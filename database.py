import sqlite3
import os

DB_PATH= os.path.join(os.path.dirname(__file__), "sports.db")

#open connection with foreign key enforcement and row dict access
def get_connection():
    conn= sqlite3.connect(DB_PATH)
    conn.row_factory= sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

#create all 8 tables if they do not exist yet
def init_db():
    conn= get_connection()
    conn.cursor().executescript("""
        CREATE TABLE IF NOT EXISTS competition (
            id   TEXT PRIMARY KEY,
            slug TEXT NOT NULL,
            name TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS stage (
            id              TEXT PRIMARY KEY,
            _competition_id TEXT NOT NULL,
            name            TEXT NOT NULL,
            ordering        INTEGER NOT NULL,
            FOREIGN KEY (_competition_id) REFERENCES competition(id)
        );
        CREATE TABLE IF NOT EXISTS match_group (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            _stage_id TEXT NOT NULL,
            name      TEXT NOT NULL,
            FOREIGN KEY (_stage_id) REFERENCES stage(id)
        );
        CREATE TABLE IF NOT EXISTS team (
            id            TEXT PRIMARY KEY,
            name          TEXT NOT NULL,
            official_name TEXT,
            slug          TEXT,
            abbreviation  TEXT,
            country_code  TEXT
        );
        CREATE TABLE IF NOT EXISTS match (
            id                  INTEGER PRIMARY KEY AUTOINCREMENT,
            _competition_id     TEXT NOT NULL,
            _stage_id           TEXT NOT NULL,
            _group_id           INTEGER,
            _home_team_id       TEXT,
            _away_team_id       TEXT,
            season              INTEGER,
            date_venue          TEXT,
            time_venue_utc      TEXT,
            status              TEXT,
            stadium             TEXT,
            description         TEXT,
            home_stage_position INTEGER,
            away_stage_position INTEGER,
            FOREIGN KEY (_competition_id) REFERENCES competition(id),
            FOREIGN KEY (_stage_id)       REFERENCES stage(id),
            FOREIGN KEY (_group_id)       REFERENCES match_group(id),
            FOREIGN KEY (_home_team_id)   REFERENCES team(id),
            FOREIGN KEY (_away_team_id)   REFERENCES team(id)
        );
        CREATE TABLE IF NOT EXISTS match_result (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            _match_id       INTEGER NOT NULL UNIQUE,
            home_goals      INTEGER,
            away_goals      INTEGER,
            _winner_team_id TEXT,
            message         TEXT,
            FOREIGN KEY (_match_id)       REFERENCES match(id),
            FOREIGN KEY (_winner_team_id) REFERENCES team(id)
        );
        CREATE TABLE IF NOT EXISTS score_by_period (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            _result_id  INTEGER NOT NULL,
            period_name TEXT NOT NULL,
            home_goals  INTEGER,
            away_goals  INTEGER,
            FOREIGN KEY (_result_id) REFERENCES match_result(id)
        );
        CREATE TABLE IF NOT EXISTS match_event (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            _match_id  INTEGER NOT NULL,
            _team_id   TEXT,
            event_type TEXT NOT NULL,
            minute     INTEGER,
            note       TEXT,
            FOREIGN KEY (_match_id) REFERENCES match(id),
            FOREIGN KEY (_team_id)  REFERENCES team(id)
        );
    """)
    conn.commit()
    conn.close()

#insert default competition, stages, teams and 5 sample matches
def seed_db():
    conn= get_connection()
    cur=  conn.cursor()

    cur.execute("INSERT OR IGNORE INTO competition (id, slug, name) VALUES (?, ?, ?)",
        ("afc-champions-league", "afc-champions-league", "AFC Champions League"))

    cur.executemany("INSERT OR IGNORE INTO stage (id, _competition_id, name, ordering) VALUES (?, ?, ?, ?)", [
        ("ROUND OF 16", "afc-champions-league", "ROUND OF 16", 4),
        ("FINAL",       "afc-champions-league", "FINAL",       7),
    ])

    cur.executemany("INSERT OR IGNORE INTO team (id, name, official_name, slug, abbreviation, country_code) VALUES (?,?,?,?,?,?)", [
        ("al-shabab-fc","Al Shabab","Al Shabab FC","al-shabab-fc","SHA", "KSA"),
        ("fc-nasaf-qarshi","Nasaf","FC Nasaf","fc-nasaf-qarshi","NAS", "UZB"),
        ("al-hilal-saudi-fc","Al Hilal","Al Hilal Saudi FC","al-hilal-saudi-fc","HIL","KSA"),
        ("shabab-al-ahli-club", "Shabab Al Ahli", "SHABAB AL AHLI DUBAI", "shabab-al-ahli-club","SAH", "UAE"),
        ("al-duhail-sc","Al Duhail","AL DUHAIL SC","al-duhail-sc","DUH", "QAT"),
        ("al-rayyan-sc","Al Rayyan","AL RAYYAN SC","al-rayyan-sc","RYN", "QAT"),
        ("al-faisaly-fc","Al Faisaly","Al Faisaly FC","al-faisaly-fc","FAI", "KSA"),
        ("foolad-khuzestan-fc", "Foolad","FOOLAD KHOUZESTAN FC", "foolad-khuzestan-fc","FLD", "IRN"),
        ("urawa-red-diamonds","Urawa Reds","Urawa Red Diamonds","urawa-red-diamonds","RED", "JPN"),
    ])

    match_ids= []
    for m in [
        ("afc-champions-league","ROUND OF 16",None, "al-shabab-fc","fc-nasaf-qarshi",2024,"2024-01-03","00:00:00","played",None),
        ("afc-champions-league","ROUND OF 16",None, "al-hilal-saudi-fc","shabab-al-ahli-club",2024,"2024-01-03","16:00:00","scheduled",None),
        ("afc-champions-league","ROUND OF 16",None, "al-duhail-sc","al-rayyan-sc",2024,"2024-01-04", "15:25:00","scheduled",None),
        ("afc-champions-league","ROUND OF 16",None, "al-faisaly-fc","foolad-khuzestan-fc", 2024, "2024-01-04","08:00:00","scheduled",None),
        ("afc-champions-league","FINAL",None,None,"urawa-red-diamonds",2024,"2024-01-19","00:00:00","scheduled",None),
    ]:
        cur.execute("INSERT INTO match (_competition_id,_stage_id,_group_id,_home_team_id,_away_team_id,season,date_venue,time_venue_utc,status,stadium) VALUES (?,?,?,?,?,?,?,?,?,?)", m)
        match_ids.append(cur.lastrowid)

    cur.execute("INSERT OR IGNORE INTO match_result (_match_id, home_goals, away_goals, _winner_team_id, message) VALUES (?,?,?,?,?)",
        (match_ids[0], 1, 2, "fc-nasaf-qarshi", None))

    conn.commit()
    conn.close()

if __name__== "__main__":
    init_db()
    seed_db()
    print("Database initialized and seeded.")