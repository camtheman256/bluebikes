import pandas as pd
import os
import datetime


def stations_present(fp):
    df = pd.read_csv(fp)
    df.rename(
        {"start station id": "start_station_id",
            "end station id": "end_station_id"},
        inplace=True, axis='columns')
    return set(df['start_station_id']) | set(df['end_station_id'])


prev_sets = set()
stations_with_dates = pd.DataFrame()
for dataset_fp in sorted(os.listdir("alltrips/data")):
    if not dataset_fp.endswith(".csv"):
        continue
    print(f"Processing dataset {dataset_fp}...")
    dataset_date = datetime.date(int(dataset_fp[:4]), int(dataset_fp[4:6]), 1)
    stations = stations_present(f"alltrips/data/{dataset_fp}")
    stations_with_dates = stations_with_dates.append(
        [{"id": station, "opened": dataset_date} for station in stations - prev_sets])
    prev_sets.update(stations)

stations_with_dates.to_csv("alltrips/new_stations.csv", index_label="idx")
