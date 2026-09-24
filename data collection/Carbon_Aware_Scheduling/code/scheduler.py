import pandas as pd
from pathlib import Path

# Find project folders
project_folder = Path(__file__).parent.parent
data_folder = project_folder / "data"

# Load data
workload = pd.read_csv(data_folder / "workload.csv")
carbon_all = pd.read_csv(
    data_folder / "real_carbon_intensity_7days.csv"
)

# Convert carbon timestamps
carbon_all["time"] = pd.to_datetime(carbon_all["time"])

# Simple power assumption
POWER_PER_CORE_WATTS = 50

# Fixed flexibility for multi-day experiment
SCHEDULING_FLEXIBILITY_MINUTES = 180


def time_to_minutes(time_string):
    time_part = str(time_string).split(" ")[-1]
    hours, minutes = map(int, time_part.split(":")[:2])
    return hours * 60 + minutes


def calculate_job_carbon(
    start_time,
    runtime_minutes,
    cpu_cores,
    carbon_data
):
    """
    Calculate carbon emissions across the entire job runtime.
    Carbon intensity is evaluated at 30-minute intervals.
    """

    start = time_to_minutes(start_time)
    end = start + runtime_minutes

    energy_per_minute_kwh = (
        cpu_cores * POWER_PER_CORE_WATTS / 1000 / 60
    )

    total_carbon = 0

    for current_time in range(start, end, 30):

        matching = carbon_data[
            carbon_data["time_minutes"] == current_time
        ]

        if matching.empty:
            raise ValueError(
                f"No carbon-intensity data for "
                f"{current_time} minutes."
            )

        carbon_intensity = matching.iloc[0][
            "carbon_intensity_gco2_kwh"
        ]

        interval_start = current_time
        interval_end = current_time + 30

        minutes_running = max(
            0,
            min(end, interval_end)
            - max(start, interval_start)
        )

        energy = (
            energy_per_minute_kwh
            * minutes_running
        )

        total_carbon += (
            energy * carbon_intensity
        )

    return total_carbon


# -----------------------------------------
# RUN EXPERIMENT FOR EACH AVAILABLE DAY
# -----------------------------------------

all_results = []
all_schedules = []

available_dates = sorted(
    carbon_all["time"].dt.strftime("%Y-%m-%d").unique()
)

print("\n===== MULTI-DAY REAL CARBON EXPERIMENT =====")
print("Days available:", len(available_dates))
print("Flexibility:", SCHEDULING_FLEXIBILITY_MINUTES, "minutes")
print()


for experiment_date in available_dates:

    print("-----------------------------------------")
    print("Experiment date:", experiment_date)

    # Select one day
    carbon = carbon_all[
        carbon_all["time"].dt.strftime("%Y-%m-%d")
        == experiment_date
    ].copy()

    # Convert timestamps to minutes since midnight
    carbon["time_minutes"] = (
        carbon["time"].dt.hour * 60
        + carbon["time"].dt.minute
    )

    # Make sure the day has usable data
    if carbon.empty:
        continue

    # -----------------------------------------
    # BASELINE
    # -----------------------------------------

    baseline = workload.copy()

    baseline["time_minutes"] = (
        baseline["arrival_time"]
        .apply(time_to_minutes)
    )

    baseline["carbon_gco2"] = baseline.apply(
        lambda job: calculate_job_carbon(
            job["arrival_time"],
            job["runtime_minutes"],
            job["cpu_cores"],
            carbon
        ),
        axis=1
    )

    baseline_total = baseline[
        "carbon_gco2"
    ].sum()

    # -----------------------------
    # CARBON-AWARE SCHEDULER
    # -----------------------------

    carbon_aware = workload.copy()

    scheduled_times = []
    scheduled_carbon = []

    for _, job in carbon_aware.iterrows():

        arrival = time_to_minutes(job["arrival_time"])
        latest_time = arrival + SCHEDULING_FLEXIBILITY_MINUTES

        # Candidate start times within the allowed flexibility window
        possible_times = carbon[
            (carbon["time_minutes"] >= arrival) &
            (carbon["time_minutes"] <= latest_time)
        ].copy()

        if possible_times.empty:
            raise ValueError(
                f"No feasible scheduling time found for job {job['job_id']}"
            )

        # Evaluate TOTAL carbon emissions for the complete job
        candidate_results = []

        for _, candidate in possible_times.iterrows():

            candidate_start = candidate["time"].strftime(
                "%Y-%m-%d %H:%M"
            )

            total_job_carbon = calculate_job_carbon(
                candidate_start,
                job["runtime_minutes"],
                job["cpu_cores"],
                carbon
            )

            candidate_results.append({
                "start_time": candidate_start,
                "start_intensity": candidate[
                    "carbon_intensity_gco2_kwh"
                ],
                "total_carbon": total_job_carbon
            })

        candidate_results = pd.DataFrame(candidate_results)

        # Select the start time with the lowest TOTAL job emissions
        best_candidate = candidate_results.loc[
            candidate_results["total_carbon"].idxmin()
        ]

        scheduled_times.append(best_candidate["start_time"])
        scheduled_carbon.append(best_candidate["start_intensity"])


    carbon_aware["scheduled_time"] = scheduled_times
    carbon_aware["carbon_intensity_gco2_kwh"] = scheduled_carbon

    carbon_aware["energy_kwh"] = (
        carbon_aware["cpu_cores"]
        * POWER_PER_CORE_WATTS
        * (carbon_aware["runtime_minutes"] / 60)
        / 1000
    )

    # Calculate actual carbon across the entire runtime
    carbon_aware["carbon_gco2"] = carbon_aware.apply(
        lambda job: calculate_job_carbon(
            job["scheduled_time"],
            job["runtime_minutes"],
            job["cpu_cores"],
            carbon
        ),
        axis=1
    )

    carbon_aware_total = (
        carbon_aware["carbon_gco2"].sum()
    )

    savings = (
        baseline_total
        - carbon_aware_total
    )

    savings_percentage = (
        savings / baseline_total
    ) * 100

    # -----------------------------------------
    # STORE RESULTS
    # -----------------------------------------

    all_results.append({
        "experiment_date": experiment_date,
        "flexibility_minutes":
            SCHEDULING_FLEXIBILITY_MINUTES,
        "usable_data_points": len(carbon),
        "baseline_carbon_gco2":
            baseline_total,
        "carbon_aware_carbon_gco2":
            carbon_aware_total,
        "carbon_savings_gco2":
            savings,
        "carbon_savings_percent":
            savings_percentage
    })

    # Store individual job schedules too
    for _, job in carbon_aware.iterrows():

        all_schedules.append({
            "experiment_date": experiment_date,
            "job_id": job["job_id"],
            "arrival_time": job["arrival_time"],
            "scheduled_time":
                job["scheduled_time"],
            "runtime_minutes":
                job["runtime_minutes"],
            "cpu_cores": job["cpu_cores"],
            "carbon_intensity_gco2_kwh":
                job[
                    "carbon_intensity_gco2_kwh"
                ],
            "carbon_gco2":
                job["carbon_gco2"]
        })

    print(
        "Baseline:",
        round(baseline_total, 2),
        "gCO2"
    )

    print(
        "Carbon-aware:",
        round(carbon_aware_total, 2),
        "gCO2"
    )

    print(
        "Savings:",
        round(savings, 2),
        "gCO2"
    )

    print(
        "Savings:",
        round(savings_percentage, 2),
        "%"
    )


# -----------------------------------------
# SAVE RESULTS
# -----------------------------------------

results_folder = project_folder / "results"
results_folder.mkdir(exist_ok=True)

results_df = pd.DataFrame(all_results)

results_df.to_csv(
    results_folder
    / "multi_day_real_carbon_results.csv",
    index=False
)

schedules_df = pd.DataFrame(all_schedules)

schedules_df.to_csv(
    results_folder
    / "multi_day_job_schedules.csv",
    index=False
)


# -----------------------------------------
# OVERALL SUMMARY
# -----------------------------------------

print("\n===== OVERALL MULTI-DAY RESULTS =====")

print(results_df)

print("\n===== SUMMARY =====")

print(
    "Average savings:",
    round(
        results_df[
            "carbon_savings_percent"
        ].mean(),
        2
    ),
    "%"
)

print(
    "Minimum savings:",
    round(
        results_df[
            "carbon_savings_percent"
        ].min(),
        2
    ),
    "%"
)

print(
    "Maximum savings:",
    round(
        results_df[
            "carbon_savings_percent"
        ].max(),
        2
    ),
    "%"
)

print(
    "\nResults saved to:"
)

print(
    "results/multi_day_real_carbon_results.csv"
)

print(
    "results/multi_day_job_schedules.csv"
)