import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

project_folder = Path(__file__).parent.parent
results_folder = project_folder / "results"

data = pd.read_csv(
    results_folder / "scenario5_workload_configuration_sensitivity.csv"
)

runtime = data[
    data["Sensitivity Variable"] == "Runtime"
]

cpu = data[
    data["Sensitivity Variable"] == "CPU cores"
]

delay = data[
    data["Sensitivity Variable"] == "Delay tolerance"
]

fig, axes = plt.subplots(
    1,
    3,
    figsize=(15, 5)
)

# Runtime sensitivity
axes[0].plot(
    runtime["Variable Value"],
    runtime["Carbon Savings (%)"],
    marker="o"
)

axes[0].set_title("Runtime Sensitivity")
axes[0].set_xlabel("Runtime (minutes)")
axes[0].set_ylabel("Carbon Savings (%)")
axes[0].grid(True, alpha=0.3)

# CPU sensitivity
axes[1].plot(
    cpu["Variable Value"],
    cpu["Carbon Savings (%)"],
    marker="o"
)

axes[1].set_title("CPU-Core Sensitivity")
axes[1].set_xlabel("CPU Cores")
axes[1].set_ylabel("Carbon Savings (%)")
axes[1].grid(True, alpha=0.3)

# Delay tolerance sensitivity
axes[2].plot(
    delay["Variable Value"],
    delay["Carbon Savings (%)"],
    marker="o"
)

axes[2].set_title("Delay-Tolerance Sensitivity")
axes[2].set_xlabel("Delay Tolerance (minutes)")
axes[2].set_ylabel("Carbon Savings (%)")
axes[2].grid(True, alpha=0.3)

fig.suptitle(
    "Workload Configuration Sensitivity",
    fontsize=14
)

plt.tight_layout()

output_file = (
    results_folder
    / "Figure_6_workload_configuration_sensitivity_final.png"
)

plt.savefig(
    output_file,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nSaved to:")
print(output_file)