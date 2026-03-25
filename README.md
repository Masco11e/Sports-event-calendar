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

_winner_team_id as a foreign key (not a string) The winner field is stored as an INTEGER FK to the teams table, not as a TEXT field containing the name. This ensures that changing a team’s name does not cause update anomalies—it is sufficient to update a single record in the teams table.

The seasons table as a separate entity The year, dates, and status of a season depend on the season, not on the match. If they were a field in events, this would violate 3NF due to a transitive dependency: events.id → season_year → season_start_date.

The “countries” table has been separated
Country codes and names are frequently used by teams and venues. Storing them as
strings in both tables would violate 3NF and lead to inconsistencies if a country's name
were to change.


# REST API — endpoints

The Flask backend provides ... REST endpoints. Each endpoint executes no more than 3 SQL queries—data is retrieved using a single SELECT statement with LEFT JOINs that combine all necessary tables at once (no N+1 issues).

| Method  | Path  | Description |
| :--- | :---: | ---: |
| Komórka 1 | Komórka 2 | Komórka 3 |

# User interface

# Tests

# Startup Instructions