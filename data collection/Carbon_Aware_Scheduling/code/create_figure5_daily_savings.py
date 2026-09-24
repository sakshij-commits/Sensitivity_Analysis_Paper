import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

project_folder = Path(__file__).parent.parent
results_folder = project_folder / "results"

results = pd.read_csv(
    results_folder / "multi_day_real_carbon_results.csv"
)

results["experiment_date"] = pd.to_datetime(
    results["experiment_date"]
)

plt.figure(figsize=(9, 5))

plt.bar(
    results["experiment_date"].dt.strftime("%b %d"),
    results["carbon_savings_percent"]
)

plt.xlabel("Date")
plt.ylabel("Carbon Savings (%)")
plt.title("Daily Carbon Savings Using Real Carbon-Intensity Data")

plt.axhline(
    y=0,
    linewidth=1
)

plt.grid(
    axis="y",
    alpha=0.3
)

plt.tight_layout()

output_file = (
    results_folder /
    "Figure_5_daily_carbon_savings.png"
)

plt.savefig(
    output_file,
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("\nFigure 5 saved to:")
print(output_file)