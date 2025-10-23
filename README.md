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

## Radar integration

Providing `RADAR_PUBLISHABLE_KEY` and `RADAR_SECRET_KEY` environment variables enables automatic address validation and geofence creation through Radar.  When those values are not present the application still works for development: new families are persisted without triggering any Radar API calls and you will see a warning in the server logs reminding you that geofences were skipped.
