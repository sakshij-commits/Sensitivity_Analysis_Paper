import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

project_folder = Path(__file__).parent.parent
results_folder = project_folder / "results"

data = pd.read_csv(
    results_folder / "scenario5_workload_configuration_sensitivity.csv"
)

runtime = data[data["Sensitivity Variable"] == "Runtime"]
cpu = data[data["Sensitivity Variable"] == "CPU cores"]
delay = data[data["Sensitivity Variable"] == "Delay tolerance"]

plt.figure(figsize=(10, 6))

plt.plot(
    runtime["Variable Value"],
    runtime["Carbon Savings (%)"],
    marker="o",
    label="Runtime"
)

plt.plot(
    cpu["Variable Value"],
    cpu["Carbon Savings (%)"],
    marker="o",
    label="CPU cores"
)

plt.plot(
    delay["Variable Value"],
    delay["Carbon Savings (%)"],
    marker="o",
    label="Delay tolerance"
)

plt.xlabel("Sensitivity Variable Value")
plt.ylabel("Carbon Savings (%)")
plt.title("Workload Configuration Sensitivity")
plt.legend()
plt.grid(True, alpha=0.3)

output_file = (
    results_folder
    / "Figure_6_workload_configuration_sensitivity.png"
)

plt.tight_layout()
plt.savefig(output_file, dpi=300)
plt.close()

print("\nSaved to:")
print(output_file)