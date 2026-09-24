import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

project_folder = Path(__file__).parent.parent
results_folder = project_folder / "results"

data = pd.read_csv(results_folder / "master_results.csv")

# Select workload experiment
workload_data = data[data["experiment"] == "Workload"].copy()

# Add the full workload result for comparison
comparison = pd.DataFrame({
    "workload": ["Full (J1-J10)", "Small (J1-J5)"],
    "carbon_savings_percent": [1.50, 1.98]
})

plt.bar(
    comparison["workload"],
    comparison["carbon_savings_percent"]
)

plt.xlabel("Workload")
plt.ylabel("Carbon Savings (%)")
plt.title("Effect of Workload Composition on Carbon Savings")

plt.grid(axis="y")

plt.savefig(
    results_folder / "workload_vs_carbon_savings.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()