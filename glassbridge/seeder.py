import pandas as pd

from .models import db, Step, Participant, Correct


def seed_data():
    db.session.query(Step).delete()
    db.session.query(Participant).delete()

    seeds = []

    ext_steps = pd.read_csv("data/steps.csv")
    for i, row in ext_steps.iterrows():
        seeds.append(
            Step(
                id=row["id"],
                correct=Correct.RIGHT if row["ac"] == "r" else Correct.LEFT,
            )
        )

    ext_participants = pd.read_csv("data/participants.csv", delimiter=";")
    for i, row in ext_participants.iterrows():
        seeds.append(
            Participant(
                nrp=row["nrp"],
                name=row["nama"],
            )
        )

    db.session.add_all(seeds)
    db.session.commit()
    print("Seeded initial data.")
