import pandas as pd
from pathlib import Path

project_folder = Path(__file__).parent.parent
results_folder = project_folder / "results"

# Results collected from the 7-day experiments
data = [
    # flexibility, baseline, carbon-aware
    (0,   327.325, 327.325),
    (0,   150.216667, 150.216667),
    (0,   209.016667, 209.016667),
    (0,   209.166667, 209.166667),
    (0,   329.716667, 329.716667),
    (0,   143.108333, 143.108333),
    (0,   231.258333, 231.258333),

    (30,  327.325, 325.008333),
    (30,  150.216667, 147.600000),
    (30,  209.016667, 208.666667),
    (30,  209.166667, 207.616667),
    (30,  329.716667, 326.375000),
    (30,  143.108333, 143.108333),
    (30,  231.258333, 227.166667),

    (60,  327.325, 322.558333),
    (60,  150.216667, 145.266667),
    (60,  209.016667, 208.666667),
    (60,  209.166667, 207.600000),
    (60,  329.716667, 323.441667),
    (60,  143.108333, 143.091667),
    (60,  231.258333, 225.200000),

    (120, 327.325, 321.308333),
    (120, 150.216667, 144.116667),
    (120, 209.016667, 208.666667),
    (120, 209.166667, 207.566667),
    (120, 329.716667, 313.858333),
    (120, 143.108333, 143.091667),
    (120, 231.258333, 222.666667),

    (180, 327.325, 313.675000),
    (180, 150.216667, 143.200000),
    (180, 209.016667, 208.666667),
    (180, 209.166667, 207.566667),
    (180, 329.716667, 297.791667),
    (180, 143.108333, 143.091667),
    (180, 231.258333, 218.516667),
]

df = pd.DataFrame(
    data,
    columns=[
        "flexibility_minutes",
        "baseline_carbon_gco2",
        "carbon_aware_carbon_gco2"
    ]
)

summary = df.groupby("flexibility_minutes").agg(
    total_baseline_gco2=("baseline_carbon_gco2", "sum"),
    total_carbon_aware_gco2=("carbon_aware_carbon_gco2", "sum")
).reset_index()

summary["total_savings_gco2"] = (
    summary["total_baseline_gco2"]
    - summary["total_carbon_aware_gco2"]
)

summary["overall_savings_percent"] = (
    summary["total_savings_gco2"]
    / summary["total_baseline_gco2"]
    * 100
)

summary = summary.round(2)

print("\n===== AGGREGATE 7-DAY FLEXIBILITY RESULTS =====")
print(summary.to_string(index=False))

output_file = results_folder / "aggregate_flexibility_results.csv"
summary.to_csv(output_file, index=False)

print("\nSaved to:")
print(output_file)