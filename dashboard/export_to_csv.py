import pandas as pd
from sqlalchemy import create_engine

# --- Setup ---
DB_URL = "<your Azure SQL connection string here>"  # replace before running
engine = create_engine(DB_URL)

# --- Export incident_report_export to CSV ---
print("Fetching data...")
df = pd.read_sql("SELECT * FROM incident_report_export", con=engine)

output_path = "incident_data_export.csv"
df.to_csv(output_path, index=False)
print(f"✅ Data exported to {output_path}")