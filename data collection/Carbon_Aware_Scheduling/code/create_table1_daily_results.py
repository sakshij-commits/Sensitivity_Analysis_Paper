import pandas as pd
from pathlib import Path

project_folder = Path(__file__).parent.parent
results_folder = project_folder / "results"

# Load the final multi-day results
results = pd.read_csv(
    results_folder / "multi_day_real_carbon_results.csv"
)

# Keep only the columns needed for the paper
table = results[
    [
        "experiment_date",
        "baseline_carbon_gco2",
        "carbon_aware_carbon_gco2",
        "carbon_savings_gco2",
        "carbon_savings_percent"
    ]
].copy()

# Rename columns for the paper
table.columns = [
    "Date",
    "Baseline Carbon (gCO2)",
    "Carbon-Aware Carbon (gCO2)",
    "Carbon Savings (gCO2)",
    "Carbon Savings (%)"
]

# Round numerical values
table["Baseline Carbon (gCO2)"] = table["Baseline Carbon (gCO2)"].round(2)
table["Carbon-Aware Carbon (gCO2)"] = table["Carbon-Aware Carbon (gCO2)"].round(2)
table["Carbon Savings (gCO2)"] = table["Carbon Savings (gCO2)"].round(2)
table["Carbon Savings (%)"] = table["Carbon Savings (%)"].round(2)

# Save paper-ready CSV
output_file = results_folder / "Table_1_daily_real_carbon_results.csv"
table.to_csv(output_file, index=False)

print("\n===== TABLE 1: DAILY REAL CARBON RESULTS =====")
print(table.to_string(index=False))

print("\nSaved to:")
print(output_file)