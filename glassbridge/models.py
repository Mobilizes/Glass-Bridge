import enum
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, Enum, event
from datetime import datetime

db = SQLAlchemy()


class Correct(enum.Enum):
    LEFT = "l"
    RIGHT = "r"


class Participant(db.Model):
    __tablename__ = "participants"

    nrp = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(128), nullable=False)


class Step(db.Model):
    __tablename__ = "steps"

    id = db.Column(db.Integer, primary_key=True)
    crossed = db.Column(db.BOOLEAN, default=False)
    correct = db.Column(Enum(Correct), nullable=False)

    # The one that takes the fall
    first_blood_id = db.Column(db.Integer, ForeignKey("participants.nrp"), nullable=True)
    first_blood = relationship("Participant", foreign_keys=[first_blood_id])
    first_blood_ts = db.Column(db.DateTime, nullable=True)

    # The first participant that doesn't die on step
    first_alive_id = db.Column(db.Integer, ForeignKey("participants.nrp"), nullable=True)
    first_alive = relationship("Participant", foreign_keys=[first_alive_id])
    first_alive_ts = db.Column(db.DateTime, nullable=True)

    # Jumps to the already known pitfall
    patrick = db.Column(db.Integer, default=0)
    # q: Why named patrick?
    # a: eya eya ya, yeye, yeye

    # Jumps after someone had already died
    recipients = db.Column(db.Integer, default=0)


@event.listens_for(Step.first_blood_id, "set")
def update_first_blood_ts(target, value, oldvalue, initiator):
    if value is not None:
        target.first_blood_ts = datetime.utcnow()


@event.listens_for(Step.first_alive_id, "set")
def update_first_alive_ts(target, value, oldvalue, initiator):
    if value is not None:
        target.first_alive_ts = datetime.utcnow()
