import random
from datetime import datetime, timedelta
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.db.db_models import IncidentReport, Base

# --- Setup ---
DB_URL = "placeholder"  # replace this locally, not in git
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
db = Session()
fake = Faker()

# --- Sample Values ---
sports = ["Soccer", "Hockey", "Football", "Basketball", "Rugby"]
age_groups = ["U10", "U12", "U14", "U16", "U18"]
roles = ["Coach", "Parent", "Trainer"]
symptom_list = ["headache", "dizziness", "nausea", "blurred_vision", "sensitivity_to_light"]
injury_contexts = [
    "Player hit head after falling during practice",
    "Collision with another player during a tackle",
    "Fell backwards while skating and hit head on ice",
    "Caught elbow to the temple during a rebound",
    "Head hit the ground diving for the ball",
    "Accidental knee to the head during a scramble",
    "Landed awkwardly after a jump and hit head"
]

# --- Data Generation ---
def generate_incident():
    now = datetime.utcnow()
    incident_date = now - timedelta(days=random.randint(0, 90))
    return IncidentReport(
        user_id=fake.uuid4(),
        timestamp=now,
        reporter_role=random.choice(roles),
        sport_type=random.choice(sports),
        age_group=random.choice(age_groups),
        team_id=fake.bothify(text="Team_##??"),
        injury_date=incident_date,
        injury_context=random.choice(injury_contexts) + ".",
        symptoms={symptom: random.randint(0, 10) for symptom in symptom_list},
        lost_consciousness=bool(random.getrandbits(1)),
        seen_provider=bool(random.getrandbits(1)),
        diagnosed_concussion=bool(random.getrandbits(1)),
        still_symptomatic=bool(random.getrandbits(1)),
        cleared_to_play=bool(random.getrandbits(1))
    )

# --- Insert Records ---
Base.metadata.create_all(engine)
print("Inserting test data...")
for _ in range(200):
    incident = generate_incident()
    db.add(incident)
db.commit()
print("Done.")

db.close()