import pandas as pd
from pathlib import Path

project_folder = Path(__file__).parent.parent
results_folder = project_folder / "results"

print("\n===== FINAL EXPERIMENT AUDIT =====\n")

# --------------------------------------------------
# Scenario 1: Scheduling Flexibility
# --------------------------------------------------

flex_file = results_folder / "aggregate_flexibility_results.csv"
flex = pd.read_csv(flex_file)

print("Scenario 1: Scheduling Flexibility")

expected_flexibility = [0, 30, 60, 120, 180]

if flex["flexibility_minutes"].tolist() == expected_flexibility:
    print("PASS: All required flexibility levels are present.")
else:
    print("CHECK: Flexibility levels are not exactly as expected.")

if flex["total_savings_gco2"].iloc[0] == 0:
    print("PASS: Zero flexibility produces zero savings.")
else:
    print("CHECK: Zero-flexibility result.")

if flex["total_savings_gco2"].is_monotonic_increasing:
    print("PASS: Absolute savings increase with flexibility.")
else:
    print("CHECK: Savings are not monotonic.")

print()

# --------------------------------------------------
# Scenario 2: Daily Real-Data Analysis
# --------------------------------------------------

daily_file = results_folder / "multi_day_real_carbon_results.csv"
daily = pd.read_csv(daily_file)

print("Scenario 2: Daily Real-Data Analysis")

if len(daily) == 7:
    print("PASS: Seven daily observations are present.")
else:
    print("CHECK: Expected seven daily observations.")

if "carbon_savings_percent" in daily.columns:
    print(
        "Average daily savings (%):",
        round(
            daily["carbon_savings_percent"].mean(),
            2
        )
    )

print()

# --------------------------------------------------
# Scenario 3: Carbon-Intensity Sensitivity
# --------------------------------------------------

master_file = results_folder / "FINAL_MASTER_RESULTS.csv"
master = pd.read_csv(master_file)

profiles = master[
    master["experiment"] == "Carbon Profile"
]

expected_profiles = {
    "Real",
    "High +50%",
    "Reversed"
}

print("Scenario 3: Carbon-Intensity Sensitivity")

actual_profiles = set(
    profiles["profile"]
)

if expected_profiles.issubset(actual_profiles):
    print(
        "PASS: Original, higher-intensity, and reversed profiles are present."
    )
else:
    print(
        "CHECK: Carbon-profile conditions are incomplete."
    )

print()

# --------------------------------------------------
# Scenario 4: Workload-Size Analysis
# --------------------------------------------------

workload_rows = master[
    master["experiment"] == "Workload Size"
]

print("Scenario 4: Workload-Size Analysis")

if "Small (J1-J5)" in workload_rows["profile"].values:
    print("PASS: Smaller workload condition is present.")
else:
    print("CHECK: Smaller workload condition is missing.")

print(
    "Workload-size rows:",
    len(workload_rows)
)

print()

# --------------------------------------------------
# Scenario 5: Workload-Configuration Sensitivity
# --------------------------------------------------

scenario5_file = (
    results_folder
    / "scenario5_workload_configuration_sensitivity.csv"
)

scenario5 = pd.read_csv(scenario5_file)

print(
    "Scenario 5: Workload-Configuration Sensitivity"
)

expected_variables = {
    "Runtime",
    "CPU cores",
    "Delay tolerance"
}

actual_variables = set(
    scenario5["Sensitivity Variable"]
)

if expected_variables.issubset(actual_variables):
    print(
        "PASS: Runtime, CPU-core, and delay-tolerance sensitivity are present."
    )
else:
    print(
        "CHECK: Scenario 5 sensitivity variables are incomplete."
    )

if len(scenario5) == 15:
    print("PASS: All 15 Scenario 5 conditions are present.")
else:
    print(
        "CHECK: Expected 15 Scenario 5 rows."
    )

print()

# --------------------------------------------------
# Overall result
# --------------------------------------------------

print("===== AUDIT SUMMARY =====")

scenario_results = [
    len(flex) == 5,
    len(daily) == 7,
    expected_profiles.issubset(actual_profiles),
    "Small (J1-J5)" in workload_rows["profile"].values,
    expected_variables.issubset(actual_variables)
    and len(scenario5) == 15
]

if all(scenario_results):
    print(
        "PASS: All five Chapter 3 experimental scenarios have result data."
    )
else:
    print(
        "CHECK: One or more experimental scenarios require review."
    )

print("\nAudit complete.\n")