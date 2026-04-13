import click
from flask import Flask
from werkzeug.security import generate_password_hash

from api.infra.db.models.base_model import Base
from api.infra.db.models.user_model import UserModel
from api.infra.db.session import SessionLocal, engine


def init_db_command(app: Flask) -> None:
    @app.cli.command("init-db")
    def init_db() -> None:
        Base.metadata.create_all(bind=engine)

        click.echo("Database initialized.")


def create_admin_command(app: Flask) -> None:
    @app.cli.command("create-admin")
    def create_admin() -> None:
        name = click.prompt("Name")
        email = click.prompt("Email")
        password = click.prompt("Password", hide_input=True, confirmation_prompt=True)

        db = SessionLocal()
        try:
            existing = db.query(UserModel).filter_by(email=email).first()
            if existing:
                click.echo(f"Error: a user with email '{email}' already exists.")
                return

            user = UserModel(
                name=name,
                email=email,
                password=generate_password_hash(password),
                role="admin",
                is_active=True,
            )
            db.add(user)
            db.commit()
            click.echo(f"Admin '{name}' created successfully.")
        finally:
            db.close()
