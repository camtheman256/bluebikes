import pandas as pd
import datetime
import json
import os
from functools import reduce
import pytz

eastern = pytz.timezone("US/Eastern")


def parse_dataset(fp):
    station_info = json.load(open(f"data/{fp}"))
    station_df = pd.DataFrame(station_info["data"]["stations"])
    station_df["last_updated"] = datetime.datetime.fromtimestamp(station_info["last_updated"], pytz.utc).astimezone(eastern)
    return station_df

big_df = reduce(lambda df, new: df.append(new), (parse_dataset(fp) for fp in os.listdir('data')))
big_df.to_csv("station_statuses.csv", index_label='idx')