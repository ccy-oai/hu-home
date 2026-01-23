# Hu's Home
Hu's Home (pronounced "who's home") is an app that tracks whether everybody in a family is home.
This repo contains Hu's Home's WebSocket server and a simple web client.

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

On macOS/Linux, activate the virtual environment with `source venv/bin/activate` instead.

## Try it out
http://127.0.0.1:5000/
