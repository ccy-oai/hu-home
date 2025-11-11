# Hu's Home
Hu's home (pronounced - who's home) is an app to track if everybody in a family is home
This repo contains Hu's home websocket server and a simple web client

Fun fact: the developers like to say that if someone asks, "Who's home?" you can answer, "Hu's home"—and that's the kind of joke that never gets old.

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
