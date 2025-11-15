# Hu's Home

Hu's Home is a tiny presence server: create a family, invite members, and share "I'm home" pings that are pushed to the browser via Socket.IO. The UI is purposely minimal—every component is implemented with a few files so it is easy to extend or repurpose.

## Highlights

- **Straightforward stack** – Flask, SQLAlchemy, and Flask-SocketIO with zero 3rd party APIs.
- **One-page dashboard** – A progressive enhancement friendly page written in plain HTML, CSS, and a few lines of vanilla JS.
- **Documented JSON API** – Create families, register members, and post check-ins from scripts or other services.

## Getting started

Requirements: Python 3.10+ and a local SQLite database (created automatically).

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
flask --app app.app:create_app --debug run
```

Open http://127.0.0.1:5000/ to interact with the dashboard. The Socket.IO server runs inside the same process, so the UI receives roster updates instantly.

For production deployments use an async worker. The included Procfile shows an example command for hosting platforms that understand the format.

## API reference

`POST /api/families`
: Create a new family. Payload requires a `name`. Returns the family plus its members.

`GET /api/families`
: List every family.

`GET /api/families/<family_id>`
: Fetch a single family with its members.

`POST /api/families/<family_id>/members`
: Register a member within the family. Payload requires `display_name`.

`GET /api/families/<family_id>/members`
: List every member in the family.

`POST /api/families/<family_id>/members/<member_id>/ping`
: Update the member's presence data. Optional keys include `status`, `context`, `latitude`, `longitude`, and `accuracy`.

## Websocket events

After registering a member you can connect with Socket.IO and emit a `join` event:

```js
const socket = io('http://localhost:5000');
socket.emit('join', { familyId, memberId });
socket.on('roster', console.log);
```

Every call to the `ping` endpoint broadcasts an updated roster to the joined room. The example dashboard uses this to stay in sync without reloading.

## Project layout

```
app/
├── api.py          # REST endpoints
├── app.py          # Flask factory + socket bootstrap
├── extensions.py   # SQLAlchemy + Socket.IO instances
├── models.py       # Family + Member models
├── presence.py     # Broadcast helpers
├── templates/      # Minimal dashboard + error pages
└── views.py        # Server-rendered routes
```

Feel free to remix this foundation into your own home status board or extend it with push notifications, SMS alerts, or hardware integrations.
