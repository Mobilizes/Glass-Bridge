import os
from dotenv import load_dotenv

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
        # team = submission["team_id"]
        # if team != senopati_external_team_id:
        #     continue

        submission = Submission.query.filter_by(id=id).first()
        if submission is not None:
            continue

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
            db.session.rollback()
            continue

        participant = Participant.query.filter_by(nrp=nrp).first()
        if participant is None:
            db.session.rollback()
            continue

        print(f"Nama: {nama}, id: {id}")

        second_try = False
        if participant.first_try is None:
            participant.first_try_id = id
            print("First Try!")
        elif participant.second_try is None:
            participant.second_try_id = id
            second_try = True
            print("Second Try!")
        else:
            print("HOW DID THIS HAPPEN")
            db.session.rollback()
            continue

        try:
            r = s.get(f"https://www.its.ac.id/informatika/domjudge/jury/submissions/{id}")
            soup = BeautifulSoup(r.text, "html.parser")
            body = soup.find("body")
            td = body.find_all("td")[1]
            testcases = td.find_all("a")

            accepted = True
            for i, testcase in enumerate(testcases):
                if not accepted:
                    break

                verdict = testcase.get_text()
                if verdict != "✓":
                    if steps[i].stepped:
                        steps[i].patricks += 1
                    print(f"Verdict on step {i}: {verdict}")
                    accepted = False
                elif not second_try:
                    steps[i].survivors += 1

                steps[i].stepped = True
                db.session.add(steps[i])

            if accepted:
                print("AC!")
        except Exception as e:
            print(e)
            db.session.rollback()

        db.session.commit()
