# Hu's Home
Hu's home (pronounced - who's home) is an app to track if everybody in a family is home
This repo contains Hu's home websocket server and a simple web client

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

## Project Structure

The repository contains both the Socket.IO enabled Flask backend and a
lightweight browser client. A quick tour of the most important folders:

- `app/app.py` – application factory and Socket.IO initialization.
- `app/routes/` – REST-style view functions used by the web client.
- `app/controllers/` & `app/services/` – business logic that powers the
  websocket events.
- `app/static/` & `app/templates/` – the vanilla JS/HTML frontend served
  directly by Flask.

Understanding where each responsibility lives should make it easier to jump
into the codebase and extend Hu's Home.
