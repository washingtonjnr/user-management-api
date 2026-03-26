from flask import Flask

from api.config.spec import spec
from api.entrypoints.blueprints import app_bp
from api.entrypoints.blueprints.health import health_route
from api.infra.db.models.base_model import Base
from api.infra.db.session import engine


def create_app() -> Flask:
    app = Flask(__name__)

    spec.register(app)

    _register_db()

    _register_blueprints(app)

    return app


def _register_db() -> None:
    Base.metadata.create_all(bind=engine)


def _register_blueprints(app: Flask) -> None:
    app.register_blueprint(health_route)

    app.register_blueprint(app_bp, url_prefix="/api")


if __name__ == "__main__":
    app = create_app()

    app.run()
