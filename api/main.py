from flask import Flask

from api.config.spec import spec


def create_app() -> Flask:
    app = Flask(__name__)

    spec.register(app)

    _register_db()
    _register_blueprints(app)
    _register_commands(app)

    return app


def _register_db() -> None:
    from api.infra.db.models.base_model import Base
    from api.infra.db.session import engine

    Base.metadata.create_all(bind=engine)


def _register_blueprints(app: Flask) -> None:
    from api.entrypoints.blueprints import app_bp
    from api.entrypoints.blueprints.health import health_route

    app.register_blueprint(health_route)

    app.register_blueprint(app_bp, url_prefix="/api")


def _register_commands(app: Flask) -> None:
    from api.config.commands import create_admin_command, init_db_command

    init_db_command(app)
    create_admin_command(app)


if __name__ == "__main__":
    app = create_app()

    app.run()
