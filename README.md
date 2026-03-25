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

HTML5/CSS3/JS - Application frontend, Single Page Application without external JavaScript frameworks

pytest - Backend unit and integration tests.

# Project file structure



# Database



## Key design decisions (3NF)

"_winner_team_id" as a foreign key. The winner field in match_result stores an foreign key to the team table, not text containing the team name. Changing a team's name requires updating only one record in the team table—all relationships remain intact.

"stage" as a separate entity The “name” and “ordering” fields for a stage depend on the stage itself, not on the match.

"_competition_id" as a foreign key in the stage table. The league name and slug depend on the league, not on the competition stage. If they were fields in the stage table, changing the league name would require updating every stage record

"match_group" as a separate entity. The group name is specific to the group, not the match.

"match_result" as a separate entity. The match result (home_goals, away_goals, _winner_team_id) constitutes a separate fact, it may not exist for matches that have not been played.

"score_by_period" as a separate entity. Subsection scores (first half, overtime) depend on the match result, not directly on the match itself. Saving them as columns in "match_result" would prevent the flexible addition of new periods without changing the schema.

"match_event" as a separate entity. Match events (goals, minutes) are repeated multiple times during a single match. 

"_home_team_id" and "_away_team_id" as foreign keys. Team data (official name, abbreviation, country code) is specific to the team, not the match.

# REST API — endpoints

The Flask backend provides ... REST endpoints. Each endpoint executes no more than 3 SQL queries—data is retrieved using a single SELECT statement with LEFT JOINs that combine all necessary tables at once (no N+1 issues).

| Method  | Path  | Description |
| :--- | :---: | ---: |
| Komórka 1 | Komórka 2 | Komórka 3 |

# User interface

# Tests

# Startup Instructions