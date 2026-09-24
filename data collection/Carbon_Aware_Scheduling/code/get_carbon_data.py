import requests
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

# Find our project folder
project_folder = Path(__file__).parent.parent
data_folder = project_folder / "data"

# Number of historical days to collect
DAYS = 7

# Use the date of the existing experiment as the reference date
end_date = datetime.now(ZoneInfo("Asia/Kolkata")).date()
start_date = end_date - timedelta(days=DAYS - 1)

rows = []

print(f"Collecting carbon-intensity data from {start_date} to {end_date}...")

for i in range(DAYS):

    current_date = start_date + timedelta(days=i)

    url = f"https://api.carbonintensity.org.uk/intensity/date/{current_date}"

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()["data"]

    for entry in data:

        # API timestamps are UTC
        utc_time = datetime.fromisoformat(
            entry["from"].replace("Z", "+00:00")
        )

        # Convert UTC → IST
        ist_time = utc_time.astimezone(
            ZoneInfo("Asia/Kolkata")
        )

        actual_intensity = entry["intensity"]["actual"]

        # Keep only records where actual intensity exists
        if actual_intensity is not None:

            rows.append({
                "time": ist_time.strftime("%Y-%m-%d %H:%M"),
                "carbon_intensity_gco2_kwh": actual_intensity
            })


carbon = pd.DataFrame(rows)

# Remove duplicate timestamps
carbon = carbon.drop_duplicates(
    subset=["time"]
).sort_values("time")

# Save to CSV
output_file = data_folder / "real_carbon_intensity_7days.csv"

carbon.to_csv(
    output_file,
    index=False
)

print("\nReal carbon-intensity data saved to:")
print(output_file)

print("\nFirst 10 records:")
print(carbon.head(10))

print("\nLast 10 records:")
print(carbon.tail(10))

print("\nDataset information:")
print("Rows:", len(carbon))
print("Missing values:", carbon["carbon_intensity_gco2_kwh"].isna().sum())
print("Start:", carbon["time"].min())
print("End:", carbon["time"].max())