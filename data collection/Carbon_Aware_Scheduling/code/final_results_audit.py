import pandas as pd
from pathlib import Path

project_folder = Path(__file__).parent.parent
results_folder = project_folder / "results"

TOLERANCE = 0.01

print("===== FINAL RESULTS AUDIT =====")

# -----------------------------
# LOAD FINAL FILES
# -----------------------------

master = pd.read_csv(
    results_folder / "FINAL_MASTER_RESULTS.csv"
)

flex = pd.read_csv(
    results_folder / "aggregate_flexibility_results.csv"
)

daily = pd.read_csv(
    results_folder / "multi_day_real_carbon_results.csv"
)

tables = pd.ExcelFile(
    results_folder / "FINAL_PAPER_TABLES.xlsx"
)

# -----------------------------
# CHECK 1 — FLEXIBILITY DATA
# -----------------------------

print("\n[1] FLEXIBILITY RESULTS")

expected_flexibility = [0, 30, 60, 120, 180]
actual_flexibility = sorted(
    flex["flexibility_minutes"].tolist()
)

print("Expected:", expected_flexibility)
print("Found:   ", actual_flexibility)

assert actual_flexibility == expected_flexibility
print("PASS")

# -----------------------------
# CHECK 2 — BASELINE CONSISTENCY
# -----------------------------

print("\n[2] BASELINE CONSISTENCY")

baseline_values = flex[
    "total_baseline_gco2"
].round(2).unique()

print("Baseline values:", baseline_values)

assert len(baseline_values) == 1
print("PASS: Baseline is constant across flexibility levels.")

# -----------------------------
# CHECK 3 — ZERO FLEXIBILITY
# -----------------------------

print("\n[3] ZERO FLEXIBILITY")

zero = flex[
    flex["flexibility_minutes"] == 0
].iloc[0]

print(
    "Baseline:",
    zero["total_baseline_gco2"]
)

print(
    "Carbon-aware:",
    zero["total_carbon_aware_gco2"]
)

print(
    "Savings:",
    zero["overall_savings_percent"],
    "%"
)

assert abs(
    zero["overall_savings_percent"]
) < TOLERANCE

print("PASS")

# -----------------------------
# CHECK 4 — MONOTONIC SAVINGS
# -----------------------------

print("\n[4] MONOTONIC FLEXIBILITY TREND")

ordered = flex.sort_values(
    "flexibility_minutes"
)

savings = ordered[
    "overall_savings_percent"
].tolist()

print("Savings:", savings)

assert all(
    savings[i] <= savings[i + 1] + TOLERANCE
    for i in range(len(savings) - 1)
)

print("PASS")

# -----------------------------
# CHECK 5 — DAILY DATA
# -----------------------------

print("\n[5] DAILY RESULTS")

print("Days:", len(daily))

assert len(daily) == 7

print(
    "Minimum daily savings:",
    round(
        daily["carbon_savings_percent"].min(),
        2
    ),
    "%"
)

print(
    "Maximum daily savings:",
    round(
        daily["carbon_savings_percent"].max(),
        2
    ),
    "%"
)

print("PASS")

# -----------------------------
# CHECK 6 — MASTER RESULTS
# -----------------------------

print("\n[6] MASTER RESULTS")

print(
    "Master rows:",
    len(master)
)

assert len(master) == 9

print("PASS: 9 master experiment rows found.")

# -----------------------------
# CHECK 7 — PAPER TABLES
# -----------------------------

print("\n[7] PAPER TABLES")

expected_sheets = [
    "Table 1 - Daily",
    "Table 2 - Flexibility",
    "Table 3 - Profile",
    "Table 4 - Workload"
]

print("Found sheets:", tables.sheet_names)

assert tables.sheet_names == expected_sheets

print("PASS")

# -----------------------------
# CHECK 8 — KEY FINAL RESULT
# -----------------------------

print("\n[8] KEY FINAL RESULT")

best = flex.loc[
    flex["overall_savings_percent"].idxmax()
]

print(
    "Best flexibility:",
    int(best["flexibility_minutes"]),
    "minutes"
)

print(
    "Savings:",
    round(
        best["overall_savings_percent"],
        2
    ),
    "%"
)

print(
    "CO2 saved:",
    round(
        best["total_savings_gco2"],
        2
    ),
    "gCO2"
)

# -----------------------------
# COMPLETE
# -----------------------------

print("\n================================")
print("ALL FINAL RESULTS AUDIT CHECKS PASSED")
print("================================")
print("\nExperimental results are ready to freeze.")