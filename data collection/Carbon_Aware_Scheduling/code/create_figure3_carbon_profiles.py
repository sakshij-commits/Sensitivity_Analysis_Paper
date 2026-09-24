import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

project_folder = Path(__file__).parent.parent
results_folder = project_folder / "results"

# Load final master results
results = pd.read_csv(
    results_folder / "FINAL_MASTER_RESULTS.csv"
)

# Select carbon-profile experiments
profiles = results[
    results["experiment"] == "Carbon Profile"
].copy()

# Create figure
plt.figure(figsize=(8, 5))

plt.bar(
    profiles["profile"],
    profiles["carbon_savings_percent"]
)

plt.xlabel("Carbon-Intensity Profile")
plt.ylabel("Carbon Savings (%)")
plt.title("Effect of Carbon-Intensity Profile on Carbon Savings")

plt.grid(
    axis="y",
    alpha=0.3
)

plt.tight_layout()

# Save publication-quality figure
output_file = (
    results_folder /
    "Figure_3_carbon_profile_sensitivity.png"
)

plt.savefig(
    output_file,
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("\nFigure 3 saved to:")
print(output_file)