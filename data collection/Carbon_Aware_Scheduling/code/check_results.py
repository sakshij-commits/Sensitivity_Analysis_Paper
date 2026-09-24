import pandas as pd
from pathlib import Path

project_folder = Path(__file__).parent.parent
results_folder = project_folder / "results"

data = pd.read_csv(results_folder / "master_results.csv")

print("\n===== MASTER EXPERIMENT RESULTS =====\n")
print(data.to_string(index=False))

print("\n===== EXPERIMENT COUNTS =====\n")
print(data["experiment"].value_counts())

print("\n===== SAVINGS SUMMARY =====\n")
print(
    data[
        [
            "experiment",
            "carbon_profile",
            "flexibility_minutes",
            "carbon_savings_gco2",
            "carbon_savings_percent"
        ]
    ].to_string(index=False)
)

print("\n===== BEST OBSERVED SAVINGS =====\n")

best = data.loc[data["carbon_savings_percent"].idxmax()]

print("Experiment:", best["experiment"])
print("Profile:", best["carbon_profile"])
print("Flexibility:", best["flexibility_minutes"], "minutes")
print("Savings:", best["carbon_savings_gco2"], "gCO2")
print("Savings percentage:", best["carbon_savings_percent"], "%")