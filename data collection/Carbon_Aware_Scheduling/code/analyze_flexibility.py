import pandas as pd
from pathlib import Path

project_folder = Path(__file__).parent.parent
results_folder = project_folder / "results"

data = pd.read_csv(results_folder / "paper_results_table.csv")

x = data["Scheduling Flexibility (min)"]
y = data["Carbon Savings (%)"]

# Linear trend
slope, intercept = __import__("numpy").polyfit(x, y, 1)

print("\nFLEXIBILITY ANALYSIS")
print("--------------------")

print("Minimum flexibility:", x.min(), "minutes")
print("Maximum flexibility:", x.max(), "minutes")

print("Savings at minimum flexibility:",
      y.iloc[0], "%")

print("Savings at maximum flexibility:",
      y.iloc[-1], "%")

print("Increase in savings:",
      round(y.iloc[-1] - y.iloc[0], 2), "percentage points")

print("Average savings:",
      round(y.mean(), 2), "%")

print("Linear trend slope:",
      round(slope, 4),
      "percentage points per minute")

print("\nRESULT:")
print(
    "Carbon savings increased from",
    y.iloc[0],
    "% to",
    y.iloc[-1],
    "% as scheduling flexibility increased from",
    x.min(),
    "to",
    x.max(),
    "minutes."
)