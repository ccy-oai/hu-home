# Hu's Home

Hu's Home (pronounced "who's home") is a small Flask application that keeps
track of whether the members of a family are currently at home.  A Firebase
client authenticates each person, location data is pushed to Radar, and the
server fans out realtime updates over Socket.IO so that every client subscribed
to the same family sees the same roster.

The repository contains a classic Flask app structure (blueprints, controllers,
models, and services), a websocket server implemented with Flask-SocketIO, and
static assets for the single-page client that lives under `app/templates` and
`app/static`.

## Requirements

* Python 3.9+
* `pip` (ships with Python) and a virtual environment tool such as `venv`
* A Radar account and Firebase service account credentials (used for geofencing
  and authentication)
* Optional: PostgreSQL when you do not want to use the default SQLite database

## Local development

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate            # Windows: .venv\\Scripts\\activate

# 2. Install the dependencies
pip install -r requirements.txt

# 3. Tell Flask how to find the factory and enable debug mode
export FLASK_APP=app.app:create_app   # Windows (PowerShell): $Env:FLASK_APP="app.app:create_app"
export FLASK_ENV=development

# 4. Start the websocket-enabled development server
flask run                             # The client is served from http://127.0.0.1:5000/
```

The server automatically creates any missing tables when it boots.  When the
`DATABASE_URL` environment variable is not set, a SQLite database file called
`temp.db` is created in the project directory.

### Environment configuration

Create a `.env` file (loaded by `python-dotenv`) or export the variables in your
shell before running the server.

| Variable | Description |
| --- | --- |
| `FLASK_ENV` | Set to `development` to enable debugging locally. |
| `DATABASE_URL` | SQLAlchemy connection string (defaults to SQLite). |
| `SECRET_KEY` | Session and CSRF secret used by Flask. |
| `PROJECT_ID`, `CLIENT_EMAIL`, `PRIVATE_KEY`, `PRIVATE_KEY_ID`, `CLIENT_ID`, `TYPE`, `AUTH_URI`, `TOKEN_URI`, `AUTH_PROVIDER_X590_CERT_URL`, `CLIENT_X509_CERT_URL` | Firebase Admin SDK service account values. Remember to replace literal `\n` in the private key with real newlines. |
| `API_KEY`, `AUTH_DOMAIN`, `STORAGE_BUCKET`, `MESSAGING_SENDER_ID`, `APP_ID`, `MEASUREMENT_ID` | Firebase client configuration returned to the browser. |
| `RADAR_PUBLISHABLE_KEY`, `RADAR_SECRET_KEY` | Keys for the Radar API used for geofencing lookups. |

## API and websocket surface

The following endpoints are registered in addition to the web client:

| Endpoint | Description |
| --- | --- |
| `GET /api/client-config` | Returns Firebase and Radar config values that the browser client consumes. |
| `GET /api/get-user` | Authenticates the Firebase user associated with the bearer token and returns the profile plus any family data. |
| `POST /api/family` | Creates a new family, writes the Radar geofence, and assigns the requesting user as a member. |
| `POST /update/event` | Webhook endpoint that Radar uses to push geofence events into the websocket roster. |
| `Socket.IO /update` | Clients connect with `x-client-id` and `x-family-id` headers to receive `roster` events in realtime. |

These routes live under `app/routes` and `app/socketio.py` if you want to see
how the logic is implemented.

## Production notes

The included `Procfile` runs the app with Gunicorn:

```bash
gunicorn --bind 0.0.0.0:$PORT app.app:create_app()
```

Make sure the environment variables above are defined in your hosting
environment and that the Radar webhook is configured to point at
`https://<your-domain>/update/event`.
