import os

from flask import Flask
from flask_migrate import Migrate
from dotenv import load_dotenv

from .models import db
from .seeder import seed_data
from . import routes


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
    Migrate(app, db)

    @app.cli.command("seed")
    def seed_command():
        with app.app_context():
            seed_data()

    app.register_blueprint(routes.bp)

    return app
