import pandas as pd
from pathlib import Path

project_folder = Path(__file__).parent.parent
results_folder = project_folder / "results"
results_folder.mkdir(exist_ok=True)

rows = []

# --------------------------------------------------
# 1. FLEXIBILITY EXPERIMENT — 7 DAYS, REAL DATA
# --------------------------------------------------

flexibility_results = [
    (0,   1599.81, 1599.81),
    (30,  1599.81, 1585.54),
    (60,  1599.81, 1575.83),
    (120, 1599.81, 1561.28),
    (180, 1599.81, 1532.51),
]

for flexibility, baseline, carbon_aware in flexibility_results:
    savings = baseline - carbon_aware
    percentage = savings / baseline * 100

    rows.append({
        "experiment": "Scheduling Flexibility",
        "profile": "Real 7-Day Data",
        "flexibility_minutes": flexibility,
        "baseline_carbon_gco2": baseline,
        "carbon_aware_carbon_gco2": carbon_aware,
        "carbon_savings_gco2": savings,
        "carbon_savings_percent": percentage
    })


# --------------------------------------------------
# 2. CARBON PROFILE EXPERIMENT
# --------------------------------------------------

carbon_profile_results = [
    ("Real",      231.26, 227.80, 3.46, 1.50),
    ("High +50%", 346.89, 341.70, 5.19, 1.50),
    ("Reversed",  191.68, 183.50, 8.18, 4.27),
]

for profile, baseline, carbon_aware, savings, percentage in carbon_profile_results:

    rows.append({
        "experiment": "Carbon Profile",
        "profile": profile,
        "flexibility_minutes": 60,
        "baseline_carbon_gco2": baseline,
        "carbon_aware_carbon_gco2": carbon_aware,
        "carbon_savings_gco2": savings,
        "carbon_savings_percent": percentage
    })


# --------------------------------------------------
# 3. WORKLOAD SIZE EXPERIMENT
# --------------------------------------------------

rows.append({
    "experiment": "Workload Size",
    "profile": "Small (J1-J5)",
    "flexibility_minutes": 60,
    "baseline_carbon_gco2": 112.85,
    "carbon_aware_carbon_gco2": 110.62,
    "carbon_savings_gco2": 2.23,
    "carbon_savings_percent": 1.98
})


# --------------------------------------------------
# CREATE FINAL MASTER TABLE
# --------------------------------------------------

final_results = pd.DataFrame(rows)

final_results["baseline_carbon_gco2"] = (
    final_results["baseline_carbon_gco2"].round(2)
)

final_results["carbon_aware_carbon_gco2"] = (
    final_results["carbon_aware_carbon_gco2"].round(2)
)

final_results["carbon_savings_gco2"] = (
    final_results["carbon_savings_gco2"].round(2)
)

final_results["carbon_savings_percent"] = (
    final_results["carbon_savings_percent"].round(2)
)


# Save final master results
output_file = results_folder / "FINAL_MASTER_RESULTS.csv"

final_results.to_csv(
    output_file,
    index=False
)

print("\n===== FINAL MASTER RESULTS =====")
print(final_results.to_string(index=False))

print("\nSaved to:")
print(output_file)