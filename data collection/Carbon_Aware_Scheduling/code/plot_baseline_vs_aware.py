import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

project_folder = Path(__file__).parent.parent
results_folder = project_folder / "results"

data = pd.read_csv(results_folder / "master_results.csv")

flexibility = data[data["experiment"] == "Flexibility"].copy()

plt.plot(
    flexibility["flexibility_minutes"],
    flexibility["baseline_carbon_gco2"],
    marker="o",
    label="Baseline"
)

plt.plot(
    flexibility["flexibility_minutes"],
    flexibility["carbon_aware_carbon_gco2"],
    marker="o",
    label="Carbon-Aware"
)

plt.xlabel("Scheduling Flexibility (minutes)")
plt.ylabel("Carbon Emissions (gCO2)")
plt.title("Baseline vs Carbon-Aware Scheduling")

plt.legend()
plt.grid(True)

plt.savefig(
    results_folder / "baseline_vs_carbon_aware.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()