import os
from dotenv import load_dotenv
from datetime import datetime

import requests
import json
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup

from glassbridge import create_app, db
from glassbridge.models import Step, Submission, Participant

load_dotenv()

username = os.getenv("DOMJUDGE_USERNAME")
password = os.getenv("DOMJUDGE_PASSWORD")
contest_external_id = os.getenv("DOMJUDGE_CONTEST_EID")
senopati_external_team_id = os.getenv("DOMJUDGE_SENOPATI_EID")

s = requests.Session()
r = s.get("https://www.its.ac.id/informatika/domjudge/login")
soup = BeautifulSoup(r.text, "html.parser")
token = soup.find("input", {"name": "_csrf_token"})["value"]

login = s.post(
    "https://www.its.ac.id/informatika/domjudge/login",
    data={"_username": username, "_password": password, "_csrf_token": token},
)

r = s.get(
    f"https://www.its.ac.id/informatika/domjudge/api/v4/contests/{contest_external_id}/submissions",
    headers={"Accept": "application/json"},
    auth=HTTPBasicAuth(username, password),
)

data = json.loads(r.content)

app = create_app()

with app.app_context():
    steps = Step.query.all()

    for submission in data:
        id = submission["id"]
        # INFO: Dont forget to turn this uncomment this upon production
        team = submission["team_id"]
        sub_time = datetime.fromisoformat(submission["time"])
        if team != senopati_external_team_id:
            continue

        submission = Submission.query.filter_by(id=id).first()
        if submission is not None and submission.check_count == 2:
            continue

        if submission is not None:
            new_submission = submission
            new_submission.check_count += 1
        else:
            new_submission = Submission(id=id)
        db.session.add(new_submission)

        r = s.get(
            f"https://www.its.ac.id/informatika/domjudge/jury/submissions/{id}/source"
        )
        try:
            soup = BeautifulSoup(r.text, "html.parser")
            text_layer = soup.find("div", class_="editor")
            code = text_layer.text.split("\n")

            nama = code[1][13:]
            nrp = code[2][17:]
            nrp = nrp[: nrp.index("@")]
        except Exception:
            print(f"Submission ID {id} error; failed to fetch name or nrp")
            db.session.commit()
            continue

        participant = Participant.query.filter_by(nrp=nrp).first()
        if participant is None:
            print(f"Submission ID {id} error; nrp is not participant")
            db.session.commit()
            continue

        filler = True
        second_try = False
        if int(id) not in participant.all_submissions:
            if participant.first_try is None:
                participant.first_try_id = id
                filler = False

            elif participant.filler_try_id_1 is None:
                participant.filler_try_id_1 = id
            elif participant.filler_try_id_2 is None:
                participant.filler_try_id_2 = id
            elif participant.filler_try_id_3 is None:
                participant.filler_try_id_3 = id
            elif participant.filler_try_id_4 is None:
                participant.filler_try_id_4 = id

            elif participant.second_try is None:
                participant.second_try_id = id
                second_try = True
                filler = False
            else:
                print(f"Submission ID {id} error; {nrp} has 3 or more submissions!")
                db.session.rollback()
                continue
        elif participant.first_try_id is not None and id == participant.first_try_id:
            filler = False
        elif participant.second_try_id is not None and id == participant.second_try_id:
            second_try = True
            filler = False

        print(
            f"nama: {nama}, first try: {not second_try}, submission id: {id}, check count: {submission.check_count if submission is not None else 0}"
        )

        try:
            r = s.get(
                f"https://www.its.ac.id/informatika/domjudge/jury/submissions/{id}"
            )
            soup = BeautifulSoup(r.text, "html.parser")
            body = soup.find("body")
            td = body.find_all("td")[1]
            testcases = td.find_all("a")

            accepted = True
            for i, testcase in enumerate(testcases):
                if not accepted:
                    break

                if (
                    (not second_try or i > participant.first_try.step)
                    and not filler and submission is None
                ):
                    steps[i].survivors += 1

                verdict = testcase.get_text()
                if verdict != "✓":
                    if steps[i].stepped and not filler and submission is None:
                        steps[i].patricks += 1
                    print(f"Verdict on step {i}: {verdict}")
                    accepted = False
                new_submission.step = i
                db.session.add(new_submission)

                if not steps[i].stepped:
                    steps[i].first_step_nrp = nrp
                    steps[i].first_step_ts = sub_time
                steps[i].stepped = True
                steps[i].latest_step_nrp = nrp
                steps[i].latest_step_ts = sub_time
                db.session.add(steps[i])

            if accepted:
                print("AC!")
        except Exception as e:
            print("Unknown error:", repr(e))
            db.session.rollback()

        db.session.commit()
