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

## Health check endpoint

The API exposes a lightweight health check that can be used by uptime monitors or load balancer probes:

```
curl http://127.0.0.1:5000/api/health
```

The response includes the deployment environment and whether the instance is running with debug mode enabled.
