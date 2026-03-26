from flask import Flask

from api.config.settings import settings
from api.entrypoints.blueprints import app_bp
from api.entrypoints.blueprints.health import health_route


def create_app() -> Flask:
    app = Flask(__name__)

    app.config["JWT_SECRET_KEY"] = settings.jwt_secret_key
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = settings.jwt_access_token_expires

    _register_blueprints(app)

    return app


def _register_blueprints(app: Flask) -> None:
    app.register_blueprint(health_route)

    app.register_blueprint(app_bp, url_prefix="/api")


if __name__ == "__main__":
    app = create_app()

    app.run()
