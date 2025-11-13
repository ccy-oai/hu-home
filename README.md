# Hu's Home
Hu's home (pronounced - who's home) is an app to track if everybody in a family is home
This repo contains Hu's home websocket server and a simple web client

# Project Overview
- **Realtime presence tracking** – the Flask server exposes websocket endpoints that keep every
  connected client up to date as people come and go.
- **Lightweight web UI** – a minimal client in `app/` displays the current state without requiring
  a native install.
- **Single-command setup** – once a virtual environment is created you only need `flask run` to
  start developing locally.

# Local Development

## Initial
```
python -m pip install --user virtualenv
virtualenv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Running Server
```
venv\Scripts\activate
flask run
```

## Try it out
http://127.0.0.1:5000/
