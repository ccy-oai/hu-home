# Hu's Home

Hu's Home (pronounced "who's home") is a Flask + Socket.IO application that keeps track of which family members are currently at home. The repository contains the websocket-enabled backend as well as the web client that renders the roster updates pushed from the server.

## Tech stack

- [Flask](https://flask.palletsprojects.com/) application factory (`app/app.py`) with Jinja templates located in `app/templates/`
- [Flask-SocketIO](https://flask-socketio.readthedocs.io/) channels configured in `app/socketio.py` to broadcast roster updates in real time
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) database models stored in `app/models/`
- [Firebase Admin SDK](https://firebase.google.com/docs/admin/setup) and [Radar](https://radar.com/) integrations configured via environment variables in `app/settings.py`

## Requirements

- Python 3.8+
- A working [virtual environment](https://docs.python.org/3/library/venv.html) (`venv`, `virtualenv`, or your preferred tool)
- Firebase service account credentials and Radar API keys if you want to exercise the external integrations

## Initial setup

1. **Create and activate a virtual environment** (choose the command that matches your platform):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # macOS / Linux
   .venv\Scripts\activate        # Windows PowerShell or Command Prompt
   ```

2. **Install dependencies**:

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Provide configuration via environment variables**. The app loads values from a local `.env` file through `python-dotenv`, so the easiest approach is to create a copy of `.env` in the project root. At minimum you will want values similar to the following:

   ```dotenv
   FLASK_ENV=development
   SECRET_KEY=dev-secret
   DATABASE_URL=sqlite:///$(pwd)/temp.db

   # Firebase Admin SDK
   PROJECT_ID=your-project-id
   PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
   CLIENT_EMAIL=firebase-adminsdk@example.iam.gserviceaccount.com
   TYPE=service_account
   PRIVATE_KEY_ID=...
   CLIENT_ID=...
   AUTH_URI=https://accounts.google.com/o/oauth2/auth
   TOKEN_URI=https://oauth2.googleapis.com/token
   AUTH_PROVIDER_X590_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
   CLIENT_X509_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/...

   # Firebase client bundle (used by the browser)
   API_KEY=...
   AUTH_DOMAIN=your-project.firebaseapp.com
   STORAGE_BUCKET=your-project.appspot.com
   MESSAGING_SENDER_ID=...
   APP_ID=1:123:web:abc
   MEASUREMENT_ID=G-XXXX

   # Radar credentials (optional unless you are sending location updates)
   RADAR_PUBLISHABLE_KEY=prj_test_pk_...
   RADAR_SECRET_KEY=prj_test_sk_...
   ```

   Any values you omit default to the ones defined in `app/settings.py`. If you do not need the Firebase or Radar integrations for local work you can keep the defaults or populate them with placeholder values.

## Running the development server

With the virtual environment activated and the `.env` file in place, start the Flask development server:

```bash
export FLASK_APP="app.app:create_app"  # `set` on Windows PowerShell / CMD
export FLASK_ENV=development            # enables debug reloading
flask run --host 0.0.0.0 --port 5000
```

You should now be able to open http://127.0.0.1:5000/ and see the Hu's Home client. When testing socket connections locally, keep the terminal open to watch the connection logs.

## Production-style run

The repository includes a `Procfile` that runs Gunicorn with the same application factory used above. You can mimic that locally (after installing dependencies) with:

```bash
gunicorn --bind 0.0.0.0:5000 "app.app:create_app()"
```

This is the recommended way to run the server when deploying to platforms such as Heroku or Railway because it gives you access to multiple workers and better websocket support.

## Helpful references

- API routes are defined under `app/routes/`.
- Socket.IO event handlers and helper endpoints live in `app/socketio.py`.
- HTML templates and static assets are located in `app/templates/` and `app/static/`.
- Database models are defined in `app/models/` and are automatically created when the app starts thanks to `register_database` in `app/app.py`.

Feel free to open an issue or submit a pull request if you improve the onboarding experience or discover missing documentation.
