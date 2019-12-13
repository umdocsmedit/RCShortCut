import logging
import time
import pandas as pd  # type: ignore
import umredcap

logging.basicConfig(level=logging.DEBUG)

token: str = umredcap.creds.configuration.load()['new_redcap']

main_project: umredcap.Project = umredcap.Project()

records: pd.DataFrame = main_project.export_event_records()

current_time: time.struct_time = time.localtime()
year: int = current_time.tm_year
mo: int = current_time.tm_mon
day: int = current_time.tm_mday

records.to_csv(f"~/Desktop/backup_{year}{mo}{day}.csv", index=False)
