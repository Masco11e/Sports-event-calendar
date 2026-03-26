# Sports event calendar 

## Project description 

Sports Calendar is a web application designed to manage a calendar of sporting events. The system allows you to store, view, and add competitions across various sports, along with full details about teams, venues, and results.

This project is primarily based on the backend, while the frontend of the application was developed to visualize data and demonstrate its potential uses. The database created for this project complies with Third Normal Form (3NF).

## Project objectives: 

- Storing sports events from various disciplines.
- View the events calendar in a clear and "easy to use web" interface.
- Filter events by discipline, status, and date range.
- Adding new events using a form with validation.
- Importing data from external sources in JSON format
- Save the data to a JSON file so that another user can use it.

# System Architecture

## Technology stack

Python 3/Flask  - Application backend, HTTP server, REST endpoint routing.

SQLite - Relational database, local file, no server configuration.

HTML5/CSS/JS - Application frontend, Single Page Application without external JavaScript frameworks

pytest - Backend unit and integration tests.

# Database

[Diagram(ERD)](Diagram(ERD).pdf)

## Key design decisions (3NF)

"_winner_team_id" as a foreign key. The winner field in match_result stores an foreign key to the team table, not text containing the team name. Changing a team's name requires updating only one record in the team table—all relationships remain intact.

"stage" as a separate entity The “name” and “ordering” fields for a stage depend on the stage itself, not on the match.

"_competition_id" as a foreign key in the stage table. The league name and slug depend on the league, not on the competition stage. If they were fields in the stage table, changing the league name would require updating every stage record

"match_group" as a separate entity. The group name is specific to the group, not the match.

"match_result" as a separate entity. The match result (home_goals, away_goals, _winner_team_id) constitutes a separate fact, it may not exist for matches that have not been played.

"score_by_period" as a separate entity. Subsection scores (first half, overtime) depend on the match result, not directly on the match itself. Saving them as columns in "match_result" would prevent the flexible addition of new periods without changing the schema.

"match_event" as a separate entity. Match events (goals, minutes) are repeated multiple times during a single match. 

"_home_team_id" and "_away_team_id" as foreign keys. Team data is specific to the team, not the match.

# REST API — endpoints

The Flask backend provides 7 REST endpoints.

| Method | Path | Description |
| :--- | :--- | :--- |
| GET | /api/matches | List all matches, filterable by competition, status, date_from, date_to |
| GET | /api/matches/\<id> | Single match with full details, events and score by periods |
| POST | /api/matches | Create a new match. Auto-creates competition if name not found |
| GET | /api/competitions | List all competitions |
| GET | /api/stages | List all stages ordered by ordering field |
| POST | /api/import | Import matches from JSON in the source format |
| GET | /api/export | Export all matches to JSON in the source format |

# User interface

**index.html** — main matches page with:
- Match grid displaying competition, teams, score or kickoff time, date and status badge
- Filter bar (competition dropdown, status dropdown, date range inputs)
- Click on a card opens a detail modal with full match info and events
- "Add Match" button opens a form modal with client-side field validation

**pages/teams.html** — teams subpage (work in progress)

**pages/stats.html** — statistics subpage (work in progress)

# Tests

Tests are located in `tests/test_app.py` and cover the full backend.

| Class | Tests | What is covered |
| :--- | :---: | :--- |
| TestDatabase | 6 | Table creation, seed data, foreign key constraints |
| TestGetMatches | 9 | Status 200, match count, required fields, all filters |
| TestGetMatch | 4 | Status 200, 404 for missing, events list, score by periods |
| TestCreateMatch | 4 | Status 201, response ID, match in list, 400 for missing field |
| TestCompetitions | 2 | Status 200, seeded competition present |
| TestPages | 3 | index, teams and stats pages return 200 |

python -m pytest tests/ -v

# Startup Instructions

Install dependencies

```bash
pip install -r requirements.txt
```

Start the server
```bash
python app.py
```

Open http://localhost:8080

Optional 

You can delete and recreate the database if needed

```bash
python database.py
```