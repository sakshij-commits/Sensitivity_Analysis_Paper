import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

project_folder = Path(__file__).parent.parent
results_folder = project_folder / "results"

# Load final aggregate flexibility results
results = pd.read_csv(
    results_folder / "aggregate_flexibility_results.csv"
)

# Create figure
plt.figure(figsize=(8, 5))

plt.plot(
    results["flexibility_minutes"],
    results["overall_savings_percent"],
    marker="o",
    linewidth=2
)

plt.xlabel("Scheduling Flexibility (minutes)")
plt.ylabel("Overall Carbon Savings (%)")
plt.title("Effect of Scheduling Flexibility on Carbon Savings")

plt.xticks(
    results["flexibility_minutes"]
)

plt.grid(True, alpha=0.3)
plt.tight_layout()

# Save publication-quality figure
output_file = (
    results_folder /
    "Figure_2_flexibility_vs_carbon_savings.png"
)

plt.savefig(
    output_file,
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("\nFigure 2 saved to:")
print(output_file)