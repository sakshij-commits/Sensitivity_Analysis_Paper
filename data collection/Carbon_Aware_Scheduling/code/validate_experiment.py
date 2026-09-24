import pandas as pd
from pathlib import Path

project_folder = Path(__file__).parent.parent
data_folder = project_folder / "data"
results_folder = project_folder / "results"

# -----------------------------
# LOAD INPUT DATA
# -----------------------------

workload = pd.read_csv(data_folder / "workload.csv")
carbon = pd.read_csv(
    data_folder / "real_carbon_intensity_7days.csv"
)

# -----------------------------
# BASIC DATA VALIDATION
# -----------------------------

print("===== INPUT DATA VALIDATION =====")

print("\nWorkload:")
print("Jobs:", len(workload))
print("Columns:", list(workload.columns))

print("\nCarbon dataset:")
print("Rows:", len(carbon))
print("Missing values:")
print(carbon.isna().sum())

# Check duplicate timestamps
carbon["time"] = pd.to_datetime(carbon["time"])

duplicates = carbon["time"].duplicated().sum()

print("\nDuplicate carbon timestamps:", duplicates)

# Check carbon range
print(
    "Carbon intensity range:",
    carbon["carbon_intensity_gco2_kwh"].min(),
    "to",
    carbon["carbon_intensity_gco2_kwh"].max(),
    "gCO2/kWh"
)

# -----------------------------
# WORKLOAD VALIDATION
# -----------------------------

print("\n===== WORKLOAD VALIDATION =====")

print(
    "Unique job IDs:",
    workload["job_id"].nunique()
)

print(
    "Duplicate job IDs:",
    workload["job_id"].duplicated().sum()
)

print(
    "Runtime range:",
    workload["runtime_minutes"].min(),
    "to",
    workload["runtime_minutes"].max(),
    "minutes"
)

print(
    "CPU range:",
    workload["cpu_cores"].min(),
    "to",
    workload["cpu_cores"].max()
)

# -----------------------------
# FINAL FLEXIBILITY RESULTS
# -----------------------------

print("\n===== FINAL FLEXIBILITY RESULTS =====")

flex_file = results_folder / "aggregate_flexibility_results.csv"

if flex_file.exists():

    flex = pd.read_csv(flex_file)

    print(flex.to_string(index=False))

    # Check that all expected flexibility levels exist
    expected = {0, 30, 60, 120, 180}
    actual = set(flex["flexibility_minutes"])

    print("\nExpected flexibility levels:", expected)
    print("Found flexibility levels:", actual)

    if expected == actual:
        print("PASS: All flexibility levels present.")
    else:
        print("WARNING: Flexibility levels do not match.")

    # Check 0-minute result
    zero = flex[
        flex["flexibility_minutes"] == 0
    ].iloc[0]

    if abs(zero["overall_savings_percent"]) < 0.0001:
        print("PASS: 0-minute flexibility produces 0% savings.")
    else:
        print("WARNING: 0-minute result is not zero.")

    # Check monotonicity
    ordered = flex.sort_values("flexibility_minutes")

    savings = ordered[
        "overall_savings_percent"
    ].tolist()

    if all(
        savings[i] <= savings[i + 1]
        for i in range(len(savings) - 1)
    ):
        print(
            "PASS: Savings increase monotonically "
            "with flexibility."
        )
    else:
        print(
            "NOTE: Savings are not monotonically increasing."
        )

else:
    print(
        "aggregate_flexibility_results.csv "
        "not found."
    )

print("\n===== VALIDATION COMPLETE =====")