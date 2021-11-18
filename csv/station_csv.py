# Bluebikes publishes this data as a CSV already, so this is actually useful because we need the
# GBFS station IDs, which they do _not_ publish in the station list dataset.

import pandas as pd
import requests

station_info = requests.get("https://gbfs.bluebikes.com/gbfs/en/station_information.json").json()
station_df = pd.DataFrame(station_info["data"]["stations"])
station_df["last_updated"] = station_info["last_updated"]

station_df.to_csv("stations.csv", index_label='idx')