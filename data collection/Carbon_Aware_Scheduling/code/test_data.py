import pandas as pd
from pathlib import Path

project_folder = Path(__file__).parent.parent
data_folder = project_folder / "data"

workload = pd.read_csv(data_folder / "workload.csv")
carbon = pd.read_csv(data_folder / "carbon_intensity.csv")

# Simple assumption: each CPU core uses 50 watts
POWER_PER_CORE_WATTS = 50

# Match each job with the carbon intensity at its arrival time
jobs = workload.merge(
    carbon,
    left_on="arrival_time",
    right_on="time",
    how="left"
)

# Calculate energy used in kWh
jobs["energy_kwh"] = (
    jobs["cpu_cores"]
    * POWER_PER_CORE_WATTS
    * (jobs["runtime_minutes"] / 60)
    / 1000
)

# Calculate carbon emissions in grams
jobs["carbon_gco2"] = (
    jobs["energy_kwh"]
    * jobs["carbon_intensity_gco2_kwh"]
)

print(jobs[
    [
        "job_id",
        "arrival_time",
        "runtime_minutes",
        "cpu_cores",
        "carbon_intensity_gco2_kwh",
        "energy_kwh",
        "carbon_gco2"
    ]
])

print("\nTOTAL ENERGY:", jobs["energy_kwh"].sum(), "kWh")
print("TOTAL CARBON:", jobs["carbon_gco2"].sum(), "gCO2")