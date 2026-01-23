# Hu's Home
Hu's home (pronounced - who's home) is an app to track if everybody in a family is home
This repo contains Hu's home websocket server and a simple web client

# Local Development

## Initial
```
python -m pip install --user virtualenv
virtualenv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

## Running Server
```
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # macOS/Linux
flask run
```

## Try it out
http://127.0.0.1:5000/
