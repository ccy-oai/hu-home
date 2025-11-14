# Hu's Home

Hu's Home (pronounced *"who's home"*) is a Flask + Socket.IO application that lets a family check
who is currently home by streaming geolocation updates from each family member's device.  The
repository contains both the HTTP + WebSocket server as well as a lightweight web client that can be
used for manual testing.

## Features

- **Firebase authentication** – all API calls expect a Firebase ID token and the backend verifies it
  using the Firebase Admin SDK before returning any family data.
- **Realtime location roster** – Socket.IO keeps every connected client in sync with everyone else's
  latest GPS reading.
- **Radar geofencing** – addresses entered by a family are looked up in Radar and a 100m geofence is
  created so you can tell when somebody enters or exits the area.
- **Simple persistence** – SQLAlchemy models (SQLite by default) store families and users so the
  roster survives restarts.

## Repository layout

```
app/
 ├─ app.py              Flask application factory and extension registration
 ├─ controllers/        Traditional HTTP endpoints (home page)
 ├─ routes/             JSON API endpoints (authentication, family creation, config)
 ├─ services/           Integrations such as Radar
 ├─ socketio.py         Socket.IO server and events
 ├─ templates/          Basic HTML client used for manual testing
 └─ static/             Client assets (favicon, etc.)
```

## Prerequisites

- Python 3.9+ and pip
- A Firebase project configured for email/password (or any) authentication with a corresponding
  service account JSON
- A [Radar](https://radar.com/) account and API keys
- (Optional) PostgreSQL if you do not want to use the default SQLite database created in the project
  directory

## Getting started

1. **Clone and create a virtual environment**
   ```bash
   git clone https://github.com/<you>/hu-home.git
   cd hu-home
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```
2. **Install dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
3. **Create a `.env` file** (see the next section for details) so that the settings module can load
   your secrets.
4. **Initialize the database** by running the application once; SQLAlchemy will create all tables
   automatically on startup.

## Environment variables

Hu's Home relies entirely on environment variables that are loaded from `.env` during development via
`python-dotenv`.  The table below describes the available settings.

| Variable | Description |
| --- | --- |
| `FLASK_ENV` | `development` enables debugger + hot reload. Defaults to `production`. |
| `FLASK_APP` | Set to `app` when using the `flask` CLI. |
| `DATABASE_URL` | SQLAlchemy connection string. Defaults to a local SQLite `temp.db`. |
| `SECRET_KEY` | Flask session secret. |
| `API_KEY`, `AUTH_DOMAIN`, `PROJECT_ID`, `STORAGE_BUCKET`, `MESSAGING_SENDER_ID`, `APP_ID`, `MEASUREMENT_ID` | Firebase web client configuration returned to `/api/client-config`. |
| `TYPE`, `PRIVATE_KEY_ID`, `PRIVATE_KEY`, `CLIENT_EMAIL`, `CLIENT_ID`, `AUTH_URI`, `TOKEN_URI`, `AUTH_PROVIDER_X590_CERT_URL`, `CLIENT_X509_CERT_URL` | Firebase Admin SDK credentials used to verify ID tokens. These correspond to the fields from your service account JSON. Remember to wrap the private key in quotes and replace literal line breaks with `\n` when storing it in `.env`. |
| `RADAR_PUBLISHABLE_KEY`, `RADAR_SECRET_KEY` | Radar API keys for the JavaScript client (`publishable`) and the backend geofence creation (`secret`). |

## Running the server

```bash
# 1. Activate the virtual environment
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2. Ensure the environment variables above are exported (or present in .env)
export FLASK_APP=app
export FLASK_ENV=development

# 3. Start the development server
flask run
```

Open http://127.0.0.1:5000/ to load the simple Socket.IO client.  Grant the browser permission to
use geolocation and you should see your device appear in the roster that is broadcast to every
connected session.

For production-like testing you can run the exact command used by the Procfile:

```bash
gunicorn --bind 0.0.0.0:8000 app.app:create_app()
```

## API quick reference

| Endpoint | Method | Description |
| --- | --- | --- |
| `/api/client-config` | `GET` | Returns the Firebase + Radar publishable configuration for the frontend. |
| `/api/get-user` | `GET` | Requires `Authorization: Bearer <Firebase ID token>` and responds with the authenticated user, their family and roster. |
| `/api/family` | `POST` | Authenticated endpoint used to create a new family, persist it, and create a matching Radar geofence. |

Socket.IO emits a `roster` event every time somebody connects or sends a location update and accepts
`update` messages containing `ip` + `geo` payloads from each client.

## Troubleshooting

- If you see `401 Unauthorized` errors double-check that your Firebase ID token is being sent in the
  `Authorization` header.
- Use `python -m flask routes` to verify that Flask picked up the application factory when the CLI is
  misbehaving.
- Set `DATABASE_URL=postgresql://...` when deploying to a cloud platform such as Heroku so you do not
  rely on SQLite.

Hu's Home is intentionally small so feel free to experiment with new Socket.IO events, integrate a
mobile client, or enhance the database schema to better fit your needs.
