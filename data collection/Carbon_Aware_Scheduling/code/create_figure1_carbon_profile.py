import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

project_folder = Path(__file__).parent.parent
data_folder = project_folder / "data"
results_folder = project_folder / "results"

# Load the real 7-day carbon dataset
carbon = pd.read_csv(
    data_folder / "real_carbon_intensity_7days.csv"
)

carbon["time"] = pd.to_datetime(carbon["time"])

# Create the figure
plt.figure(figsize=(10, 5))

plt.plot(
    carbon["time"],
    carbon["carbon_intensity_gco2_kwh"],
    linewidth=1.5
)

plt.xlabel("Date and Time")
plt.ylabel("Carbon Intensity (gCO₂/kWh)")
plt.title("Real Carbon Intensity Over the 7-Day Experimental Period")

plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()

# Save high-resolution figure
output_file = results_folder / "Figure_1_real_carbon_intensity.png"

plt.savefig(
    output_file,
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("\nFigure 1 saved to:")
print(output_file)