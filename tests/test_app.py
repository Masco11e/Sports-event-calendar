import json, os, sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import database
from app import app as flask_app

@pytest.fixture(scope="session")
def test_db(tmp_path_factory):
    db_path= str(tmp_path_factory.mktemp("data") / "test.db")
    database.DB_PATH= db_path
    database.init_db()
    database.seed_db()
    yield db_path

@pytest.fixture()
def client(test_db):
    flask_app.config["TESTING"]= True
    with flask_app.test_client() as c:
        yield c

class TestDatabase:
    def test_tables_created(self, test_db):
        conn=  database.get_connection()
        names= {r["name"] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()}
        conn.close()
        assert {"competition","stage","match_group","team","match","match_result","score_by_period","match_event"}.issubset(names)

    def test_seed_competition(self, test_db):
        conn= database.get_connection()
        row=  conn.execute("SELECT * FROM competition WHERE id= 'afc-champions-league'").fetchone()
        conn.close()
        assert row is not None
        assert row["name"] == "AFC Champions League"

    def test_seed_teams(self, test_db):
        conn=  database.get_connection()
        count= conn.execute("SELECT COUNT(*) AS c FROM team").fetchone()["c"]
        conn.close()
        assert count >= 9

    def test_seed_matches(self, test_db):
        conn=  database.get_connection()
        count= conn.execute("SELECT COUNT(*) AS c FROM match").fetchone()["c"]
        conn.close()
        assert count == 5

    def test_played_result(self, test_db):
        conn= database.get_connection()
        row=  conn.execute("""
            SELECT mr.home_goals, mr.away_goals FROM match_result mr
            JOIN match m ON mr._match_id= m.id WHERE m.status= 'played' LIMIT 1
        """).fetchone()
        conn.close()
        assert row["home_goals"] == 1
        assert row["away_goals"] == 2

    def test_foreign_keys(self, test_db):
        conn= database.get_connection()
        conn.execute("PRAGMA foreign_keys = ON")
        with pytest.raises(Exception):
            conn.execute("INSERT INTO match (_competition_id,_stage_id,season,date_venue,time_venue_utc,status) VALUES ('x','x',2024,'2024-01-01','00:00:00','scheduled')")
            conn.commit()
        conn.close()

class TestGetMatches:
    def test_returns_200(self, client):
        assert client.get("/api/matches").status_code == 200

    def test_returns_5_matches(self, client):
        data= json.loads(client.get("/api/matches").data)
        assert len(data) == 5

    def test_has_required_fields(self, client):
        data= json.loads(client.get("/api/matches").data)
        for field in ("id","status","date_venue","competition_name","stage_name"):
            assert field in data[0]

    def test_filter_status_played(self, client):
        data= json.loads(client.get("/api/matches?status=played").data)
        assert all(m["status"] == "played" for m in data)

    def test_filter_status_scheduled(self, client):
        data= json.loads(client.get("/api/matches?status=scheduled").data)
        assert all(m["status"] == "scheduled" for m in data)

    def test_filter_competition(self, client):
        data= json.loads(client.get("/api/matches?competition=afc-champions-league").data)
        assert all(m["competition_id"] == "afc-champions-league" for m in data)

    def test_filter_date_range(self, client):
        data= json.loads(client.get("/api/matches?date_from=2024-01-01&date_to=2024-01-04").data)
        assert all(m["date_venue"] <= "2024-01-04" for m in data)

    def test_unknown_competition(self, client):
        data= json.loads(client.get("/api/matches?competition=does-not-exist").data)
        assert data == []

    def test_played_has_goals(self, client):
        data= json.loads(client.get("/api/matches?status=played").data)
        assert data[0]["home_goals"] is not None

class TestGetMatch:
    def test_returns_200(self, client):
        match_id= json.loads(client.get("/api/matches").data)[0]["id"]
        assert client.get(f"/api/matches/{match_id}").status_code == 200

    def test_returns_404(self, client):
        assert client.get("/api/matches/99999").status_code == 404

    def test_has_events(self, client):
        match_id= json.loads(client.get("/api/matches").data)[0]["id"]
        data=     json.loads(client.get(f"/api/matches/{match_id}").data)
        assert "events" in data
        assert isinstance(data["events"], list)

    def test_has_periods(self, client):
        match_id= json.loads(client.get("/api/matches").data)[0]["id"]
        data=     json.loads(client.get(f"/api/matches/{match_id}").data)
        assert "score_by_periods" in data

class TestCreateMatch:
    VALID= {
        "competition_name": "AFC Champions League",
        "_stage_id":        "SEMI FINAL",
        "stage_name":       "Semi Final",
        "stage_ordering":   6,
        "season":           2024,
        "date_venue":       "2024-02-15",
        "time_venue_utc":   "18:00:00",
        "status":           "scheduled",
        "home_team": {"slug": "test-home", "name": "Test Home", "abbreviation": "TSH", "country_code": "KSA"},
        "away_team": {"slug": "test-away", "name": "Test Away", "abbreviation": "TSA", "country_code": "JPN"},
    }

    def post(self, client, body):
        return client.post("/api/matches", data=json.dumps(body), content_type="application/json")

    def test_returns_201(self, client):
        assert self.post(client, self.VALID).status_code == 201

    def test_response_has_id(self, client):
        data= json.loads(self.post(client, self.VALID).data)
        assert isinstance(data["id"], int)

    def test_appears_in_list(self, client):
        body= dict(self.VALID)
        body["date_venue"]= "2024-04-01"
        self.post(client, body)
        dates= [m["date_venue"] for m in json.loads(client.get("/api/matches").data)]
        assert "2024-04-01" in dates

    def test_missing_field_400(self, client):
        assert self.post(client, {"_competition_id": "x"}).status_code == 400

class TestCompetitions:
    def test_returns_200(self, client):
        assert client.get("/api/competitions").status_code == 200

    def test_has_afc(self, client):
        data= json.loads(client.get("/api/competitions").data)
        assert any(c["id"] == "afc-champions-league" for c in data)

class TestImportExport:
    PAYLOAD= {"data": [{
        "season": 2024, "status": "played",
        "dateVenue": "2024-06-01", "timeVenueUTC": "18:00:00",
        "homeTeam": {"name": "Import A", "slug": "import-a", "abbreviation": "IMA", "teamCountryCode": "KSA"},
        "awayTeam": {"name": "Import B", "slug": "import-b", "abbreviation": "IMB", "teamCountryCode": "JPN"},
        "result": {"homeGoals": 3, "awayGoals": 0, "winner": "Import A"},
        "stage": {"id": "FINAL", "name": "FINAL", "ordering": 7},
        "originCompetitionId": "afc-champions-league",
        "originCompetitionName": "AFC Champions League",
    }]}

    def test_import_returns_201(self, client):
        res= client.post("/api/import", data=json.dumps(self.PAYLOAD), content_type="application/json")
        assert res.status_code == 201

    def test_import_count(self, client):
        res= client.post("/api/import", data=json.dumps(self.PAYLOAD), content_type="application/json")
        assert json.loads(res.data)["imported"] == 1

    def test_import_missing_data_key(self, client):
        res= client.post("/api/import", data=json.dumps({}), content_type="application/json")
        assert res.status_code == 400

    def test_export_returns_200(self, client):
        assert client.get("/api/export").status_code == 200

    def test_export_has_data_key(self, client):
        data= json.loads(client.get("/api/export").data)
        assert "data" in data
        assert isinstance(data["data"], list)

    def test_export_matches_source_format(self, client):
        data= json.loads(client.get("/api/export").data)
        record= data["data"][0]
        for field in ("season","status","dateVenue","timeVenueUTC","stage","originCompetitionId"):
            assert field in record

class TestPages:
    def test_index(self, client):
        res= client.get("/")
        assert res.status_code == 200
        assert b"Sport Calendar" in res.data

    def test_teams(self, client):
        assert client.get("/pages/teams.html").status_code == 200

    def test_stats(self, client):
        assert client.get("/pages/stats.html").status_code == 200