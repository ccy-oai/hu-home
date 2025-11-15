"""Application extensions shared across blueprints."""
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO

# A single database and socket server instance keeps the codebase tidy and
# prevents circular imports when registering handlers.
db = SQLAlchemy()
socketio = SocketIO(cors_allowed_origins="*")
