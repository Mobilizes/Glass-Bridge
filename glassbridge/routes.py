from datetime import datetime, timezone

from flask import Blueprint, render_template, current_app

from .models import Step

bp = Blueprint("index", __name__, url_prefix="/")


@bp.route("/", methods=(["GET"]))
def index():
    steps = Step.query.order_by(Step.id.asc()).all()
    end_time = (
        datetime.fromisoformat(current_app.config["END_TIME"])
        .astimezone(timezone.utc)
        .strftime("%Y-%m-%dT%H:%M:%SZ")
    )
    return render_template("index.html", steps=steps, end_time=end_time)
