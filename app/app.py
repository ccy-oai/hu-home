"""Application factory for Hu's Home."""
from __future__ import annotations

from flask import Flask, render_template

from . import settings
from .api import api
from .extensions import db, socketio
from .views import views

# Import websocket handlers for side effects so decorators register events.
from . import websocket  # noqa: F401


def create_app(config: settings.Settings | None = None) -> Flask:
    app = Flask(__name__, static_folder="static", template_folder="templates")
    active_settings = config or settings.DEFAULT_SETTINGS
    app.config.update(active_settings.flask_config)

    register_extensions(app)
    register_blueprints(app)
    register_error_handlers(app)
    return app


def register_extensions(app: Flask) -> None:
    db.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")
    with app.app_context():
        db.create_all()


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(views)
    app.register_blueprint(api)


def register_error_handlers(app: Flask) -> None:
    def render_error(error, template: str, status_code: int):
        return render_template(template), status_code

    app.register_error_handler(401, lambda e: render_error(e, "401.html", 401))
    app.register_error_handler(404, lambda e: render_error(e, "404.html", 404))
    app.register_error_handler(500, lambda e: render_error(e, "500.html", 500))


def main() -> None:
    socketio.run(create_app())


if __name__ == "__main__":
    main()

