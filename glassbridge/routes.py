import random
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
    quotes = [
        "We are humans, not horses.",
        "We are horses, not humans.",
        "Is it worth it?",
        "Also try Minecraft!",
        "Also try Terraria!",
        "And his music was electric...",
        "67",
        "Please speed I need this...",
        "My mom is kinda homeless.",
        "At the crossroad, don't turn left.",
        "Elite ball knowledge.",
        "Eya eya ya, yeye yeye.",
        "Next year for sure.",
        "Bread tastes better than key.",
        f"The #{random.randint(0, 99)} step is {random.choice(["Left", "Right"])}!",
        'The #{random.randint(0, 99)} step is {random.choice("Left", "Right")}!',
        "Fire in the hole!",
        "Maintaining the agenda is our top priority.",
        "Hungary? Then eat something.",
        "Mangos? Where does he go?",
        "Sawfish? What kind of fish tho?",
        "Beatboxer? Why would he beat a box?",
        "Royal Guard!",
        "His greed sickens me...",
        "Why is the lamp blurry?",
        "The truth is, I never went to school either...",
        "He laughed.",
        "HUUUUUUUUUUUUUUUUU",
        "Genuine question, why are people in IG racist now?",
        "Level 11 theory.",
        "Level 11 the- wait what?",
        "club penguin is kil.",
        "Jangan lupa daftar Schematics 2026!",
        "That f****** bird that I hate.",
        "And one day, I am gonna grow wings.",
        "The angel lost his wings 💔💔💔",
        "Good luck for Sistem Operasi!",
        "Absolute cinema.",
        "Do you believe in gravity?",
        "FYMTBYBF",
    ]
    quotes.append(f"There are {len(quotes)+1} quotes!")

    quote = random.choice(quotes)
    if random.random() > 0.5:
        quote = "Heavily inspired by Squid Game!"

    return render_template("index.html", steps=steps, end_time=end_time, quotes=quote)
