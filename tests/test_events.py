import pandas as pd  # type: ignore
import umredcap.events as events

from typing import List


def test_export_arms():

    arms: pd.DataFrame = events.export_arms()

    assert arms.shape[0] != 0


def test__get_num_arms():

    n_arms: int = events._get_num_arms()
    assert n_arms > 0


def test__generate_arms_list():

    # if blank it should produce an range array from 1 to max arms
    max_arms: int = events._get_num_arms()
    arms_list: List[int] = events._generate_arms_list()

    assert max(arms_list) == max_arms

    # Should simply return the list it is given otherwise
    input: List[int] = [4, 5, 6, 7]
    output: List[int] = events._generate_arms_list(input)

    assert input == output


def test_get_event_names():

    expected: List[str] = [
            '20172018_arm_4',
            '20172018_arm_5',
            '20182019_arm_4',
            '20182019_arm_5',
            ]
    arms: List[int] = [4, 5]
    prev_years = 2
    output: List[str] = events.get_event_names(
            arms,
            previous_n_years=prev_years
            )

    assert output == expected
