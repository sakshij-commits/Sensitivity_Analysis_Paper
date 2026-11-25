import pandas as pd
from pathlib import Path


# -----------------------------------------
# PROJECT PATHS
# -----------------------------------------

project_folder = Path(__file__).parent.parent
data_folder = project_folder / "data"
results_folder = project_folder / "results"

results_folder.mkdir(exist_ok=True)


# -----------------------------------------
# LOAD DATA
# -----------------------------------------

workload = pd.read_csv(
    data_folder / "workload.csv"
)

carbon_all = pd.read_csv(
    data_folder / "real_carbon_intensity_7days.csv"
)

carbon_all["time"] = pd.to_datetime(
    carbon_all["time"]
)


# -----------------------------------------
# CONTROLLED ASSUMPTIONS
# -----------------------------------------

POWER_PER_CORE_WATTS = 50
SCHEDULING_FLEXIBILITY_MINUTES = 60

RUNTIME_LEVELS = [15, 30, 60, 90, 120]


# -----------------------------------------
# HELPER FUNCTIONS
# -----------------------------------------

def time_to_minutes(time_string):

    time_part = str(time_string).split(" ")[-1]

    hours, minutes = map(
        int,
        time_part.split(":")[:2]
    )

    return hours * 60 + minutes


def calculate_job_carbon(
    start_time,
    runtime_minutes,
    cpu_cores,
    carbon_data
):

    start = time_to_minutes(start_time)
    end = start + runtime_minutes

    energy_per_minute_kwh = (
        cpu_cores
        * POWER_PER_CORE_WATTS
        / 1000
        / 60
    )

    total_carbon = 0

    for current_time in range(
        start,
        end,
        30
    ):

        matching = carbon_data[
            carbon_data["time_minutes"]
            == current_time
        ]

        if matching.empty:

            raise ValueError(
                f"No carbon-intensity data "
                f"for {current_time} minutes."
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
            energy
            * carbon_intensity
        )

    return total_carbon


# -----------------------------------------
# RUN RUNTIME EXPERIMENTS
# -----------------------------------------

all_results = []


for runtime_level in RUNTIME_LEVELS:

    print("\n====================================")
    print(
        "RUNTIME:",
        runtime_level,
        "minutes"
    )
    print("====================================")

    experiment_results = []

    available_dates = sorted(
        carbon_all["time"]
        .dt.strftime("%Y-%m-%d")
        .unique()
    )

    for experiment_date in available_dates:

        carbon = carbon_all[
            carbon_all["time"]
            .dt.strftime("%Y-%m-%d")
            == experiment_date
        ].copy()

        carbon["time_minutes"] = (
            carbon["time"].dt.hour * 60
            + carbon["time"].dt.minute
        )

        # Keep only usable carbon measurements.
        carbon = carbon.dropna(
            subset=[
                "carbon_intensity_gco2_kwh"
            ]
        )

        # -----------------------------------------
        # CREATE CONTROLLED WORKLOAD
        # -----------------------------------------

        test_workload = workload.copy()

        test_workload[
            "test_runtime_minutes"
        ] = runtime_level

        # -----------------------------------------
        # BASELINE
        # -----------------------------------------

        baseline_carbon = 0

        for _, job in test_workload.iterrows():

            baseline_carbon += calculate_job_carbon(
                job["arrival_time"],
                runtime_level,
                job["cpu_cores"],
                carbon
            )

        # -----------------------------------------
        # CARBON-AWARE
        # -----------------------------------------

        carbon_aware_carbon = 0

        for _, job in test_workload.iterrows():

            arrival = time_to_minutes(
                job["arrival_time"]
            )

            latest_time = (
                arrival
                + SCHEDULING_FLEXIBILITY_MINUTES
            )

            possible_times = carbon[
                (
                    carbon["time_minutes"]
                    >= arrival
                )
                &
                (
                    carbon["time_minutes"]
                    <= latest_time
                )
            ].copy()

            if possible_times.empty:

                raise ValueError(
                    f"No feasible candidate "
                    f"for {job['job_id']} "
                    f"on {experiment_date}"
                )

            candidate_results = []

            for _, candidate in possible_times.iterrows():

                candidate_start = (
                    candidate["time"]
                    .strftime("%Y-%m-%d %H:%M")
                )

                total_job_carbon = (
                    calculate_job_carbon(
                        candidate_start,
                        runtime_level,
                        job["cpu_cores"],
                        carbon
                    )
                )

                candidate_results.append({
                    "start_time":
                        candidate_start,
                    "total_carbon":
                        total_job_carbon
                })

            candidate_results = pd.DataFrame(
                candidate_results
            )

            best_candidate = candidate_results.loc[
                candidate_results[
                    "total_carbon"
                ].idxmin()
            ]

            carbon_aware_carbon += (
                best_candidate["total_carbon"]
            )

        # -----------------------------------------
        # SAVINGS
        # -----------------------------------------

        savings = (
            baseline_carbon
            - carbon_aware_carbon
        )

        savings_percent = (
            savings
            / baseline_carbon
        ) * 100

        experiment_results.append({
            "runtime_minutes":
                runtime_level,
            "experiment_date":
                experiment_date,
            "baseline_carbon_gco2":
                baseline_carbon,
            "carbon_aware_carbon_gco2":
                carbon_aware_carbon,
            "carbon_savings_gco2":
                savings,
            "carbon_savings_percent":
                savings_percent
        })

    # -----------------------------------------
    # AGGREGATE ACROSS 7 DAYS
    # -----------------------------------------

    daily_results = pd.DataFrame(
        experiment_results
    )

    baseline_total = (
        daily_results[
            "baseline_carbon_gco2"
        ].sum()
    )

    aware_total = (
        daily_results[
            "carbon_aware_carbon_gco2"
        ].sum()
    )

    savings_total = (
        baseline_total
        - aware_total
    )

    savings_percent_total = (
        savings_total
        / baseline_total
    ) * 100

    all_results.append({
        "runtime_minutes":
            runtime_level,
        "baseline_carbon_gco2":
            baseline_total,
        "carbon_aware_carbon_gco2":
            aware_total,
        "carbon_savings_gco2":
            savings_total,
        "carbon_savings_percent":
            savings_percent_total
    })


# -----------------------------------------
# SAVE RESULTS
# -----------------------------------------

results_df = pd.DataFrame(
    all_results
)

output_file = (
    results_folder
    / "runtime_sensitivity_results.csv"
)

results_df.to_csv(
    output_file,
    index=False
)


# -----------------------------------------
# DISPLAY RESULTS
# -----------------------------------------

print("\n====================================")
print("RUNTIME SENSITIVITY RESULTS")
print("====================================")

print(
    results_df.to_string(
        index=False
    )
)

print(
    "\nResults saved to:"
)

print(output_file)