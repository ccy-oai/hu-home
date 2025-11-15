# Hu's Home

Hu's Home (pronounced *who's home*) helps a family see who is currently checked in at the house. This repository contains a modernised Flask backend, WebSocket layer and a light-weight web client that can be used from a phone or laptop.

The 2024 refresh removes the Firebase/Radar dependency so the project can run completely locally. Everything – authentication, location tracking, real‑time updates and persistence – is powered by the Python code that lives in this repository.

## Features

* **REST API** for creating families, adding members and updating a member's status/location.
* **SQLite powered persistence** via SQLAlchemy models.
* **WebSocket roster updates** – every update instantly pushes a fresh roster to connected browsers.
* **Progressive web client** that demonstrates how to interact with the API and websocket server without installing anything.

## Getting started

The repository ships with an application factory. You can run the dev server with the built-in Flask CLI or via gunicorn.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Start the development server
flask --app app.app --debug run
```

Once the server is running visit [http://127.0.0.1:5000](http://127.0.0.1:5000) to try the new client.

### Useful commands

```bash
# Start a shell with the application context loaded
flask --app app.app shell

# Create the SQLite database (normally happens automatically on boot)
flask --app app.app init-db
```

## API overview

```
POST   /api/families                         # Create a family
GET    /api/families/<family_id>/members     # List family members
POST   /api/families/<family_id>/members     # Add a member
PATCH  /api/families/<family_id>/members/<member_id>           # Update a member profile
POST   /api/families/<family_id>/members/<member_id>/locations # Send a location ping
GET    /api/families/<family_id>/roster      # Current roster snapshot
```

The API returns JSON and every endpoint is documented inline in `app/routes/api.py`.
