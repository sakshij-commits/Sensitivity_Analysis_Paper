import pandas as pd
from pathlib import Path

project_folder = Path(__file__).parent.parent
data_folder = project_folder / "data"

# Load real carbon-intensity data
carbon = pd.read_csv(data_folder / "real_carbon_intensity.csv")

# Increase carbon intensity by 50%
carbon["carbon_intensity_gco2_kwh"] = (
    carbon["carbon_intensity_gco2_kwh"] * 1.5
)

# Save controlled carbon-intensity profile
carbon.to_csv(
    data_folder / "carbon_intensity_high.csv",
    index=False
)

print("Created carbon_intensity_high.csv")
print(carbon.head())