import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

project_folder = Path(__file__).parent.parent
results_folder = project_folder / "results"

data = pd.read_csv(results_folder / "master_results.csv")

# Select only carbon-profile experiments
profile_data = data[data["experiment"] == "Carbon Profile"]

plt.bar(
    profile_data["carbon_profile"],
    profile_data["carbon_savings_percent"]
)

plt.xlabel("Carbon-Intensity Profile")
plt.ylabel("Carbon Savings (%)")
plt.title("Effect of Carbon-Intensity Profile on Carbon Savings")

plt.grid(axis="y")

plt.savefig(
    results_folder / "carbon_profile_vs_savings.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()