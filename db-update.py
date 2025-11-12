import os
from dotenv import load_dotenv

import requests
import json
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup

from glassbridge import create_app, db
from glassbridge.models import Step, Submission

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
        db.session.commit()

        r = s.get(
            f"https://www.its.ac.id/informatika/domjudge/jury/submissions/{id}/source"
        )
        soup = BeautifulSoup(r.text, "html.parser")
        text_layer = soup.find("div", class_="editor")
        code = text_layer.text.split("\n")
        try:
            nama = code[1][13:]
            nrp = code[2][17:]
            nrp = nrp[: nrp.index("@")]
        except Exception:
            continue

        print(f"Nama: {nama}, NRP: {nrp}, ", end="")

        r = s.get(f"https://www.its.ac.id/informatika/domjudge/jury/submissions/{id}")
        soup = BeautifulSoup(r.text, "html.parser")
        body = soup.find("body")
        td = body.find_all("td")[1]
        testcases = td.find_all("a")

        accepted = True
        for i, testcase in enumerate(testcases):
            verdict = testcase.get_text()
            if verdict == "w" or verdict == "?":
                print(f"Verdict on step {i}: {verdict}")
                accepted = False
                break

        if accepted:
            print("AC!")
