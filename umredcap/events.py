import time

import umredcap.api as api
import requests
import numpy as np  # type: ignore
import pandas as pd  # type: ignore

from typing import List


def export_arms(project='new_redcap') -> pd.DataFrame:
    data = {
            'project': project,
            'content': 'arm',
            'format': 'json',
            'returnFormat': 'json'
            }

    response: requests.Response = api.request(data)
    return pd.read_json(response.text)


def export_events(project='new_redcap') -> pd.DataFrame:
    data = {
            'project': project,
            'content': 'event',
            'format': 'json',
            'returnFormat': 'json'
            }
    response: requests.Response = api.request(data)
    return pd.read_json(response.text)


def _get_num_arms() -> int:
    arms_df = export_arms()
    return arms_df.shape[0]


def _generate_arms_list(arms: List[int] = []) -> List[int]:
    total_arms = _get_num_arms()
    arms = arms if len(arms) > 0 else np.arange(0, total_arms)+1
    return arms


def _get_cur_academic_years() -> tuple:

    localtime: time.struct_time = time.localtime()
    current_year: int = localtime.tm_year
    current_month: int = localtime.tm_mon
    current_semester: str = 'fall' if current_month > 6 else 'spring'
    is_fall: bool = current_semester == 'fall'
    first_year: int = current_year if is_fall else current_year - 1
    second_year: int = current_year + 1 if is_fall else current_year

    return (first_year, second_year)


def _generate_years_list_from_n(n: int) -> List[str]:
    year_strs: List[str] = []
    first_year, second_year = _get_cur_academic_years()

    for i in range(n):
        year_1 = first_year - i - 1
        year_2 = second_year - i - 1
        year_str = f'{year_1}{year_2}'
        year_strs.append(year_str)

    year_strs.sort()
    return year_strs


def _generate_years_list_from_list(years: List[int]) -> List[str]:
    if len(years) == 0:
        return []

    year_strs: List[str] = [f'{x}{x+1}' for x in years]
    return year_strs


def _generate_years_list(years: List[int], previous_n_years: int) -> List[str]:
    prev_n_years: List[str] = _generate_years_list_from_n(previous_n_years)
    years_list: List[str] = _generate_years_list_from_list(years)
    years_list += prev_n_years
    years_list = list(set(years_list))
    years_list.sort()
    return years_list


def get_event_names(
        arms: List[int] = [],
        years: List[int] = [],
        previous_n_years: int = 0) -> List[str]:
    """Returns a list of event names given the arm numbers and either an array
    of academica years (beginning in the fall) or an integer of the previous n
    number of years. If both years, and previous_n_years are used, they are
    merged and uniqued"""

    year_strs = _generate_years_list(years, previous_n_years)
    events = []
    for year_str in year_strs:
        for arm in arms:
            event = f'{year_str}_arm_{arm}'
            events.append(event)

    events_df: pd.DataFrame = export_events()
    event_names: List[str] = events_df['unique_event_name'].to_list()
    events = [x for x in events if x in event_names]
    return events
