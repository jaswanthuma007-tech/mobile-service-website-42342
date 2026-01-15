# Mobile Service Database (SQLite)

This container stores data for the Mobile Service Website.

## Database file
- Default file: `myapp.db`

## Schema
- `services`: Service catalog for the frontend Services section
- `customer_requests`: Customer form submissions (Name, Phone, Email, Mobile Model, Problem)
- `site_content`: Basic key/value content for About/Contact

## Initialize / update schema
Run:
- `python init_db.py`

The backend reads the DB path via the `SQLITE_DB` environment variable.
