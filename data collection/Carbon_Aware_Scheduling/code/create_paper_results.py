import pandas as pd
from pathlib import Path

project_folder = Path(__file__).parent.parent
results_folder = project_folder / "results"

data = pd.read_csv(results_folder / "master_results.csv")

# Main flexibility experiment
flexibility = data[data["experiment"] == "Flexibility"].copy()

paper_table = flexibility[
    [
        "flexibility_minutes",
        "baseline_carbon_gco2",
        "carbon_aware_carbon_gco2",
        "carbon_savings_gco2",
        "carbon_savings_percent"
    ]
].copy()

paper_table.columns = [
    "Scheduling Flexibility (min)",
    "Baseline Carbon (gCO2)",
    "Carbon-Aware Carbon (gCO2)",
    "Carbon Savings (gCO2)",
    "Carbon Savings (%)"
]

# Round values for presentation
paper_table["Baseline Carbon (gCO2)"] = paper_table["Baseline Carbon (gCO2)"].round(2)
paper_table["Carbon-Aware Carbon (gCO2)"] = paper_table["Carbon-Aware Carbon (gCO2)"].round(2)
paper_table["Carbon Savings (gCO2)"] = paper_table["Carbon Savings (gCO2)"].round(2)
paper_table["Carbon Savings (%)"] = paper_table["Carbon Savings (%)"].round(2)

output_file = results_folder / "paper_results_table.csv"
paper_table.to_csv(output_file, index=False)

print("\nPAPER RESULTS TABLE\n")
print(paper_table.to_string(index=False))

print("\nSaved to:", output_file)