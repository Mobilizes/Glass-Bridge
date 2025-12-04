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

    # Senopati is uploading 3 times per submission
    filler_try_id_1 = db.Column(
        db.Integer, ForeignKey("submissions.id", ondelete="SET NULL"), nullable=True
    )

    filler_try_id_2 = db.Column(
        db.Integer, ForeignKey("submissions.id", ondelete="SET NULL"), nullable=True
    )

    filler_try_id_3 = db.Column(
        db.Integer, ForeignKey("submissions.id", ondelete="SET NULL"), nullable=True
    )

    filler_try_id_4 = db.Column(
        db.Integer, ForeignKey("submissions.id", ondelete="SET NULL"), nullable=True
    )

    second_try_id = db.Column(
        db.Integer, ForeignKey("submissions.id", ondelete="SET NULL"), nullable=True
    )
    second_try = relationship(
        "Submission", foreign_keys=[second_try_id], passive_deletes=True
    )

    @property
    def all_submissions(self):
        ids = [
            self.first_try_id,
            self.filler_try_id_1,
            self.filler_try_id_2,
            self.filler_try_id_3,
            self.filler_try_id_4,
            self.second_try_id,
        ]

        return [id for id in ids if id is not None]


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

    # Most recent one to take the step
    latest_step_nrp = db.Column(
        db.Integer, ForeignKey("participants.nrp"), nullable=True
    )
    latest_step = relationship("Participant", foreign_keys=[latest_step_nrp])
    latest_step_ts = db.Column(db.DateTime, nullable=True)

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

    # To counteract if someone submits at the same time the cronjob updates
    check_count = db.Column(db.Integer, default=0)
