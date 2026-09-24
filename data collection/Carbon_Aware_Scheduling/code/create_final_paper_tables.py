import pandas as pd
from pathlib import Path
from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter

project_folder = Path(__file__).parent.parent
results_folder = project_folder / "results"

output_file = results_folder / "FINAL_PAPER_TABLES.xlsx"

# -----------------------------
# TABLE 1 — DAILY REAL CARBON
# -----------------------------

daily = pd.read_csv(
    results_folder / "multi_day_real_carbon_results.csv"
)

table1 = daily[
    [
        "experiment_date",
        "baseline_carbon_gco2",
        "carbon_aware_carbon_gco2",
        "carbon_savings_gco2",
        "carbon_savings_percent",
    ]
].copy()

table1.columns = [
    "Date",
    "Baseline Carbon (gCO2)",
    "Carbon-Aware Carbon (gCO2)",
    "Carbon Savings (gCO2)",
    "Carbon Savings (%)",
]

# -----------------------------
# TABLE 2 — FLEXIBILITY
# -----------------------------

flex = pd.read_csv(
    results_folder / "aggregate_flexibility_results.csv"
)

table2 = flex[
    [
        "flexibility_minutes",
        "total_baseline_gco2",
        "total_carbon_aware_gco2",
        "total_savings_gco2",
        "overall_savings_percent",
    ]
].copy()

table2.columns = [
    "Scheduling Flexibility (min)",
    "Baseline Carbon (gCO2)",
    "Carbon-Aware Carbon (gCO2)",
    "Carbon Savings (gCO2)",
    "Carbon Savings (%)",
]

# -----------------------------
# TABLE 3 — CARBON PROFILE
# -----------------------------

master = pd.read_csv(
    results_folder / "FINAL_MASTER_RESULTS.csv"
)

table3 = master[
    master["experiment"] == "Carbon Profile"
][
    [
        "profile",
        "flexibility_minutes",
        "baseline_carbon_gco2",
        "carbon_aware_carbon_gco2",
        "carbon_savings_gco2",
        "carbon_savings_percent",
    ]
].copy()

table3.columns = [
    "Carbon-Intensity Profile",
    "Flexibility (min)",
    "Baseline Carbon (gCO2)",
    "Carbon-Aware Carbon (gCO2)",
    "Carbon Savings (gCO2)",
    "Carbon Savings (%)",
]

# -----------------------------
# TABLE 4 — WORKLOAD
# -----------------------------

table4 = master[
    master["experiment"] == "Workload Size"
][
    [
        "profile",
        "flexibility_minutes",
        "baseline_carbon_gco2",
        "carbon_aware_carbon_gco2",
        "carbon_savings_gco2",
        "carbon_savings_percent",
    ]
].copy()

table4.columns = [
    "Workload",
    "Flexibility (min)",
    "Baseline Carbon (gCO2)",
    "Carbon-Aware Carbon (gCO2)",
    "Carbon Savings (gCO2)",
    "Carbon Savings (%)",
]

# -----------------------------
# ROUND NUMBERS
# -----------------------------

for df in [table1, table2, table3, table4]:

    for column in df.columns:
        if "Carbon" in column or "Savings" in column:
            if column != "Carbon-Intensity Profile":
                df[column] = pd.to_numeric(
                    df[column],
                    errors="coerce"
                ).round(2)

# -----------------------------
# SAVE EXCEL WORKBOOK
# -----------------------------

with pd.ExcelWriter(
    output_file,
    engine="openpyxl"
) as writer:

    table1.to_excel(
        writer,
        sheet_name="Table 1 - Daily",
        index=False
    )

    table2.to_excel(
        writer,
        sheet_name="Table 2 - Flexibility",
        index=False
    )

    table3.to_excel(
        writer,
        sheet_name="Table 3 - Profile",
        index=False
    )

    table4.to_excel(
        writer,
        sheet_name="Table 4 - Workload",
        index=False
    )

# -----------------------------
# FORMAT WORKBOOK
# -----------------------------

wb = load_workbook(output_file)

thin_border = Border(
    left=Side(style="thin"),
    right=Side(style="thin"),
    top=Side(style="thin"),
    bottom=Side(style="thin")
)

for ws in wb.worksheets:

    # Header formatting
    for cell in ws[1]:
        cell.font = Font(bold=True)
        cell.alignment = Alignment(
            horizontal="center",
            vertical="center",
            wrap_text=True
        )
        cell.border = thin_border

    # Body formatting
    for row in ws.iter_rows(
        min_row=2,
        max_row=ws.max_row
    ):
        for cell in row:
            cell.alignment = Alignment(
                horizontal="center",
                vertical="center"
            )
            cell.border = thin_border

    # Automatic column widths
    for column_cells in ws.columns:
        max_length = 0
        column_letter = get_column_letter(
            column_cells[0].column
        )

        for cell in column_cells:
            if cell.value is not None:
                max_length = max(
                    max_length,
                    len(str(cell.value))
                )

        ws.column_dimensions[
            column_letter
        ].width = min(max_length + 3, 30)

    ws.freeze_panes = "A2"

wb.save(output_file)

print("\nFINAL PAPER TABLES CREATED")
print("---------------------------")
print("Table 1: Daily Real Carbon Results")
print("Table 2: Scheduling Flexibility Results")
print("Table 3: Carbon-Intensity Profile Sensitivity")
print("Table 4: Workload Sensitivity")
print("\nSaved to:")
print(output_file)