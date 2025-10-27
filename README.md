# Hu's Home
Hu's home (pronounced - who's home) is an app to track if everybody in a family is home.
Yes, because what the world really needed was yet another way to confirm that no one remembered to turn the lights off.
This repo contains Hu's home websocket server and a simple web client that will lovingly remind you who forgot to show up.

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
