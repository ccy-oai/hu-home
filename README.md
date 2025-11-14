# Hu's Home

Hu's Home (pronounced "who's home") is a lightweight Flask application that keeps track of who is at home by combining a REST API, a real-time Socket.IO feed, and optional Radar + Firebase integrations. The repository contains the Socket.IO server, database models, background services, and a minimal web client for quickly visualizing the roster.

## Highlights
- **Flask + Socket.IO** – exposes REST endpoints and a websocket channel that broadcasts family rosters in real time.
- **Pluggable data sources** – Firebase Admin SDK is used to authenticate devices and Radar can stream location events.
- **Single deployment target** – the included `Procfile` bootstraps the Gunicorn worker that serves the entire stack.

## Project layout
```
app/
├── app.py             # Application factory and bootstrap
├── controllers/       # Server-side rendered pages
├── routes/            # REST + websocket blueprints
├── services/          # Integrations (Radar, Firebase helpers, ...)
├── socketio.py        # Socket.IO setup and event handlers
└── templates/, static/ # Client UI
```

## Getting started
### Prerequisites
- Python 3.8+ (the versions in `requirements.txt` were validated with Python 3.8)
- A working `pip` and `virtualenv` installation

### 1. Create and activate a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate      # On Windows use: .venv\\Scripts\\activate
```

### 2. Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure the environment
Environment variables are loaded via [`python-dotenv`](https://pypi.org/project/python-dotenv/) so you can place them in a local `.env` file. At a minimum you will want:

| Variable | Purpose | Required | Default |
| --- | --- | --- | --- |
| `FLASK_ENV` | `development` enables debug mode. | No | `production` |
| `SECRET_KEY` | Flask session secret. | No | `octocat` |
| `DATABASE_URL` | SQLAlchemy connection string. Use SQLite for local dev (e.g. `sqlite:///local.db`). | No | `sqlite:///<repo>/temp.db` |
| `PROJECT_ID`, `PRIVATE_KEY`, `CLIENT_EMAIL`, `TYPE`, `PRIVATE_KEY_ID`, `CLIENT_ID`, `AUTH_URI`, `TOKEN_URI`, `AUTH_PROVIDER_X590_CERT_URL`, `CLIENT_X509_CERT_URL` | Firebase Admin service account fields. Replace newline characters in `PRIVATE_KEY` with `\n`. | Yes, if you want Firebase features | – |
| `API_KEY`, `AUTH_DOMAIN`, `STORAGE_BUCKET`, `MESSAGING_SENDER_ID`, `APP_ID`, `MEASUREMENT_ID` | Firebase client SDK config returned by the Firebase console. | Optional | – |
| `RADAR_PUBLISHABLE_KEY`, `RADAR_SECRET_KEY` | Credentials for Radar's location APIs. | Optional | – |

Save the variables as needed:
```bash
cat > .env <<'ENV'
FLASK_ENV=development
SECRET_KEY=replace-me
DATABASE_URL=sqlite:///$(pwd)/local.db
# Firebase + Radar credentials go here
ENV
```

## Running the server
Set the Flask app factory and run the development server:
```bash
export FLASK_APP=app.app:create_app
flask run
```
On Windows PowerShell:
```powershell
$env:FLASK_APP = "app.app:create_app"
flask run
```
Visit http://127.0.0.1:5000/ to confirm the roster UI loads and connects to Socket.IO.

### Production-style run
Use the same command the `Procfile` relies on:
```bash
gunicorn --bind 0.0.0.0:5000 "app.app:create_app()"
```
This mirrors the platform-as-a-service deployment configuration and is helpful for validating Gunicorn + Socket.IO locally.

## Troubleshooting
- **Firebase private key errors** – ensure the JSON is valid and newlines are encoded as `\n` in environment variables.
- **Socket.IO connection refused** – confirm the Flask server is running and that any reverse proxy forwards websocket upgrades.
- **Database schema changes** – `db.create_all()` runs automatically on startup, so remove any stale SQLite files if migrations fail.

## Next steps
The repository is intentionally minimal so that you can extend it with additional routes, scheduled jobs, or UI polish while keeping the deployment footprint small and elegant.
