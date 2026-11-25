import pandas as pd
from pathlib import Path


project_folder = Path(__file__).parent.parent
results_folder = project_folder / "results"


runtime = pd.read_csv(
    results_folder / "runtime_sensitivity_results.csv"
)

cpu = pd.read_csv(
    results_folder / "cpu_sensitivity_results.csv"
)

delay = pd.read_csv(
    results_folder / "delay_tolerance_sensitivity_results.csv"
)


runtime["variable"] = "Runtime"
runtime["condition"] = (
    runtime["runtime_minutes"].astype(str)
    + " min"
)
runtime["variable_value"] = runtime[
    "runtime_minutes"
]

cpu["variable"] = "CPU cores"
cpu["condition"] = (
    cpu["cpu_cores"].astype(str)
    + " cores"
)
cpu["variable_value"] = cpu[
    "cpu_cores"
]

delay["variable"] = "Delay tolerance"
delay["condition"] = (
    delay["delay_tolerance_minutes"].astype(str)
    + " min"
)
delay["variable_value"] = delay[
    "delay_tolerance_minutes"
]


runtime_table = runtime[
    [
        "variable",
        "condition",
        "variable_value",
        "baseline_carbon_gco2",
        "carbon_aware_carbon_gco2",
        "carbon_savings_gco2",
        "carbon_savings_percent"
    ]
].copy()

cpu_table = cpu[
    [
        "variable",
        "condition",
        "variable_value",
        "baseline_carbon_gco2",
        "carbon_aware_carbon_gco2",
        "carbon_savings_gco2",
        "carbon_savings_percent"
    ]
].copy()

delay_table = delay[
    [
        "variable",
        "condition",
        "variable_value",
        "baseline_carbon_gco2",
        "carbon_aware_carbon_gco2",
        "carbon_savings_gco2",
        "carbon_savings_percent"
    ]
].copy()


scenario5 = pd.concat(
    [
        runtime_table,
        cpu_table,
        delay_table
    ],
    ignore_index=True
)


scenario5.columns = [
    "Sensitivity Variable",
    "Condition",
    "Variable Value",
    "Baseline Carbon (gCO2)",
    "Carbon-Aware Carbon (gCO2)",
    "Carbon Savings (gCO2)",
    "Carbon Savings (%)"
]


numeric_columns = [
    "Baseline Carbon (gCO2)",
    "Carbon-Aware Carbon (gCO2)",
    "Carbon Savings (gCO2)",
    "Carbon Savings (%)"
]

scenario5[numeric_columns] = (
    scenario5[numeric_columns].round(2)
)


output_file = (
    results_folder
    / "scenario5_workload_configuration_sensitivity.csv"
)

scenario5.to_csv(
    output_file,
    index=False
)


print("\n===== SCENARIO 5 RESULTS =====\n")
print(
    scenario5.to_string(index=False)
)

print(
    "\nSaved to:",
    output_file
)