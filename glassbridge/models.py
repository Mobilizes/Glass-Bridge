import enum
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Enum, ForeignKey
from datetime import datetime

db = SQLAlchemy()


class Correct(enum.Enum):
    LEFT = "l"
    RIGHT = "r"


class Stat(db.Model):
    __tablename__ = "stats"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    nrp = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class Step(db.Model):
    __tablename__ = "steps"

    id = db.Column(db.Integer, primary_key=True)
    correct = db.Column(Enum(Correct), nullable=False)

    # The one that takes the fall
    first_blood_id = db.Column(db.Integer, ForeignKey("stats.id"), nullable=True)
    first_blood = relationship("Stat", foreign_keys=[first_blood_id])

    # The first guy that doesn't die
    first_alive_id = db.Column(db.Integer, ForeignKey("stats.id"), nullable=True)
    first_alive = relationship("Stat", foreign_keys=[first_alive_id])

    # Jumps to the already known pitfall
    patrick = db.Column(db.Integer, default=0)
    # q: Why named patrick?
    # a: eya eya ya, yeye, yeye

    # Jumps after someone had already died
    recipients = db.Column(db.Integer, default=0)
