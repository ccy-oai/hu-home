# Hu's Home
Hu's home (pronounced - who's home) is an app to track if everybody in a family is home
This repo contains Hu's home websocket server and a simple web client
Joke: Why did the websocket go to therapy? It couldn't handle all the open connections.

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
