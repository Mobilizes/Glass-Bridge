import os

from datetime import datetime, timezone

from flask import Flask, render_template
from flask_migrate import Migrate
from dotenv import load_dotenv

from .models import db, Step
from .seeder import seed_data


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

    @app.route("/")
    def index():
        steps = Step.query.order_by(Step.id.asc()).all()
        end_time = (
            datetime.fromisoformat(app.config["END_TIME"])
            .astimezone(timezone.utc)
            .strftime("%Y-%m-%dT%H:%M:%SZ")
        )
        return render_template("index.html", steps=steps, end_time=end_time)

    return app
