"""Application factory for Hu's Home."""
from __future__ import annotations

import click
from flask import Flask, render_template

from . import settings
from .database import db
from .socketio import register_socketio_events, socketio


def create_app(config_object=settings) -> Flask:
    """Create and configure a Flask application instance."""
    app = Flask(
        __name__,
        static_folder="static",
        template_folder="templates",
        instance_relative_config=False,
    )
    app.config.from_object(config_object)

    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_cli(app)

    return app


def register_extensions(app: Flask) -> None:
    """Initialise Flask extensions."""
    db.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")
    register_socketio_events()

    with app.app_context():
        db.create_all()


def register_blueprints(app: Flask) -> None:
    from .controllers.home import blueprint as home_blueprint
    from .routes.api import blueprint as api_blueprint

    app.register_blueprint(home_blueprint)
    app.register_blueprint(api_blueprint)


def register_errorhandlers(app: Flask) -> None:
    """Register human friendly error pages."""

    @app.errorhandler(401)
    def unauthorized(_: Exception):  # pragma: no cover - trivial
        return render_template("401.html"), 401

    @app.errorhandler(404)
    def not_found(_: Exception):  # pragma: no cover - trivial
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def server_error(_: Exception):  # pragma: no cover - trivial
        return render_template("500.html"), 500


def register_cli(app: Flask) -> None:
    """Expose helper commands on ``flask --app app.app``."""

    @app.cli.command("init-db")
    def init_db_command() -> None:
        """Create all tables from the current models."""
        db.drop_all()
        db.create_all()
        click.echo("Database initialised")

    @app.shell_context_processor
    def shell_context():  # pragma: no cover - developer helper
        from .models.family import Family
        from .models.user import User
        from .models.location_event import LocationEvent

        return {"db": db, "Family": Family, "User": User, "LocationEvent": LocationEvent}
