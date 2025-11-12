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

    # What step did the participant fall to?
    # Example: At step 5, participant receives WA, first_try would be 5.
    # If value is MAX+1, participant successfully crossed the entire bridge
    first_try = db.Column(db.Integer, nullable=True)
    second_try = db.Column(db.Integer, nullable=True)


class Step(db.Model):
    __tablename__ = "steps"

    id = db.Column(db.Integer, primary_key=True)
    crossed = db.Column(db.BOOLEAN, default=False)
    correct = db.Column(Enum(Correct), nullable=False)

    # The one that takes the fall
    first_blood_nrp = db.Column(
        db.Integer, ForeignKey("participants.nrp"), nullable=True
    )
    first_blood = relationship("Participant", foreign_keys=[first_blood_nrp])
    first_blood_timestamp = db.Column(db.DateTime, nullable=True)

    # The first participant that doesn't die on step
    first_alive_nrp = db.Column(
        db.Integer, ForeignKey("participants.nrp"), nullable=True
    )
    first_alive = relationship("Participant", foreign_keys=[first_alive_nrp])
    first_alive_timestamp = db.Column(db.DateTime, nullable=True)

    # How many people fell after solution is revealed
    patrick = db.Column(db.Integer, default=0)
    # q: Why named patrick?
    # a: eya eya ya, yeye, yeye

    # How many people got through this step
    survivors = db.Column(db.Integer, default=0)


class Submission(db.Model):
    __tablename__ = "submissions"

    id = db.Column(db.Integer, primary_key=True)


@event.listens_for(Step.first_blood_nrp, "set")
def update_first_blood_ts(target, value, oldvalue, initiator):
    if value is not None:
        target.first_blood_ts = datetime.utcnow()


@event.listens_for(Step.first_alive_nrp, "set")
def update_first_alive_ts(target, value, oldvalue, initiator):
    if value is not None:
        target.first_alive_ts = datetime.utcnow()
