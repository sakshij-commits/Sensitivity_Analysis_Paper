import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Find project folders
project_folder = Path(__file__).parent.parent
results_folder = project_folder / "results"

# Load experiment results
data = pd.read_csv(results_folder / "flexibility_results.csv")

# Create graph
plt.plot(
    data["flexibility_minutes"],
    data["carbon_savings_percent"],
    marker="o"
)

plt.xlabel("Scheduling Flexibility (minutes)")
plt.ylabel("Carbon Savings (%)")
plt.title("Effect of Scheduling Flexibility on Carbon Savings")

plt.grid(True)

# Save graph
plt.savefig(
    results_folder / "flexibility_vs_carbon_savings.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()