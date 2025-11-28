import os

from flask import Flask
from dotenv import load_dotenv

from .models import db
from .seeder import seed_data
from . import routes

from sqlalchemy import event
from sqlalchemy.engine import Engine
import sqlite3


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


def create_app(test_config=None):
    load_dotenv()

    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_pyfile(
            os.path.join(os.path.dirname(__file__), "config.py"), silent=False
        )
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    @app.cli.command("migrate")
    def migrate_command():
        with app.app_context():
            db.create_all()

    @app.cli.command("seed")
    def seed_command():
        with app.app_context():
            seed_data()

    app.register_blueprint(routes.bp)

    return app
