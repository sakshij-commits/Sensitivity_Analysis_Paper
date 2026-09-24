import pandas as pd
from pathlib import Path

project_folder = Path(__file__).parent.parent
data_folder = project_folder / "data"

# Load real carbon-intensity data
carbon = pd.read_csv(data_folder / "real_carbon_intensity.csv")

# Remove rows where carbon intensity is missing
carbon = carbon.dropna(
    subset=["carbon_intensity_gco2_kwh"]
).reset_index(drop=True)

# Reverse the available intensity values
carbon["carbon_intensity_gco2_kwh"] = (
    carbon["carbon_intensity_gco2_kwh"]
    .iloc[::-1]
    .reset_index(drop=True)
)

# Save reversed profile
carbon.to_csv(
    data_folder / "carbon_intensity_reversed.csv",
    index=False
)

print("Created carbon_intensity_reversed.csv")
print(carbon.head())
print("\nRows:", len(carbon))
print("Missing values:",
      carbon["carbon_intensity_gco2_kwh"].isna().sum())