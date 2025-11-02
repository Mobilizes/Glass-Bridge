import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_PATH = os.path.join(BASE_DIR, "..", "instance")

SECRET_KEY = os.getenv("SECRET_KEY")
SQLALCHEMY_DATABASE_URI = (
    f"sqlite:///{os.path.join(INSTANCE_PATH, 'glassbridge.sqlite')}"
)
SQLALCHEMY_TRACK_MODIFICATIONS = False

END_TIME = os.getenv("DOMJUDGE_END_TIME")
