from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, event
from datetime import datetime

db = SQLAlchemy()


class Participant(db.Model):
    __tablename__ = "participants"

    nrp = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(128))

    first_try_id = db.Column(
        db.Integer, ForeignKey("submissions.id", ondelete="SET NULL"), nullable=True
    )
    first_try = relationship(
        "Submission", foreign_keys=[first_try_id], passive_deletes=True
    )

    second_try_id = db.Column(
        db.Integer, ForeignKey("submissions.id", ondelete="SET NULL"), nullable=True
    )
    second_try = relationship(
        "Submission", foreign_keys=[second_try_id], passive_deletes=True
    )


class Step(db.Model):
    __tablename__ = "steps"

    id = db.Column(db.Integer, primary_key=True)
    stepped = db.Column(db.BOOLEAN, default=False)
    correct = db.Column(db.CHAR)

    # The first one to take the step
    first_step_nrp = db.Column(
        db.Integer, ForeignKey("participants.nrp"), nullable=True
    )
    first_step = relationship("Participant", foreign_keys=[first_step_nrp])
    first_step_ts = db.Column(db.DateTime, nullable=True)

    # How many people fell after solution is revealed
    patricks = db.Column(db.Integer, default=0)
    # q: Why named patrick?
    # a: eya eya ya, yeye, yeye

    # How many people got through this step
    survivors = db.Column(db.Integer, default=0)


class Submission(db.Model):
    __tablename__ = "submissions"

    id = db.Column(db.Integer, primary_key=True)

    # Example: At step 5, if participant receives WA, step would be 5.
    # If participant receives AC, step would be {LAST_STEP_INDEX+1}
    step = db.Column(db.Integer)


@event.listens_for(Step.first_step_nrp, "set")
def update_first_step_ts(target, value, oldvalue, initiator):
    if value is not None:
        target.first_step_ts = datetime.utcnow()
