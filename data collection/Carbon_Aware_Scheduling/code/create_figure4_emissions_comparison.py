import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

project_folder = Path(__file__).parent.parent
results_folder = project_folder / "results"

results = pd.read_csv(
    results_folder / "aggregate_flexibility_results.csv"
)

plt.figure(figsize=(8, 5))

plt.plot(
    results["flexibility_minutes"],
    results["total_baseline_gco2"],
    marker="o",
    linewidth=2,
    label="Baseline"
)

plt.plot(
    results["flexibility_minutes"],
    results["total_carbon_aware_gco2"],
    marker="o",
    linewidth=2,
    label="Carbon-aware"
)

plt.xlabel("Scheduling Flexibility (minutes)")
plt.ylabel("Carbon Emissions (gCO₂)")
plt.title("Baseline vs. Carbon-Aware Carbon Emissions")

plt.xticks(results["flexibility_minutes"])
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

output_file = (
    results_folder /
    "Figure_4_baseline_vs_carbon_aware.png"
)

plt.savefig(
    output_file,
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("\nFigure 4 saved to:")
print(output_file)