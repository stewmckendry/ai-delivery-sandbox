import random
from datetime import datetime, timedelta
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.db_models import IncidentReport, Base

# --- Setup ---
DB_URL = "<your Azure SQL connection string here>"  # replace this locally, not in git
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
db = Session()
fake = Faker()

# --- Sample Values ---
sports = ["Soccer", "Hockey", "Football", "Basketball", "Rugby"]
age_groups = ["U10", "U12", "U14", "U16", "U18"]
roles = ["Coach", "Parent", "Trainer"]

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
        injury_context=fake.sentence(),
        symptoms={"headache": True, "dizziness": bool(random.getrandbits(1))},
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