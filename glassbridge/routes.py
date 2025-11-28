import random
from datetime import datetime, timezone

from flask import Blueprint, render_template, current_app

from .models import Step
from .misc import quotes

bp = Blueprint("index", __name__, url_prefix="/")


@bp.route("/", methods=(["GET"]))
def index():
    steps = Step.query.order_by(Step.id.asc()).all()
    end_time = (
        datetime.fromisoformat(current_app.config["END_TIME"])
        .astimezone(timezone.utc)
        .strftime("%Y-%m-%dT%H:%M:%SZ")
    )

    quote = random.choice(quotes)

    if quote == "randomfakeanswer":
        quote = f"Step ke #{random.randint(0, 99)} adalah '{random.choice(["l", "r"])}'!"
        if random.random() < 0.2:
            quote = 'Step ke #{random.randint(0, 99)} adalah \'{random.choice("l", "r")}\'!'

    steps_json = [
        {
            "id": step.id,
            "correct": step.correct,
            "stepped": step.stepped,
            "patricks": step.patricks,
            "survivors": step.survivors,
        }
        for step in steps
    ]

    return render_template("index.html", steps=steps_json, end_time=end_time, quotes=quote)
