import time

import requests
import numpy as np  # type: ignore
import pandas as pd  # type: ignore

from umredcap.api import api
from umredcap.creds import creds
from typing import List


class arm_handler:

    def __init__(self, my_creds: creds):
        self.api = api(my_creds)

    def export_arms(self, project='new_redcap') -> pd.DataFrame:
        data = {
                'project': project,
                'content': 'arm',
                'format': 'json',
                'returnFormat': 'json'
                }

        response: requests.Response = self.api.request(data)
        return pd.read_json(response.text)

    def _get_num_arms(self) -> int:
        arms_df = self.export_arms()
        return arms_df.shape[0]

    def _generate_arms_list(self, arms: List[int] = []) -> List[int]:
        total_arms = self._get_num_arms()
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
