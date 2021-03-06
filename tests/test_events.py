import pytest  # type: ignore
import pandas as pd  # type: ignore
import umredcap.creds as creds
import umredcap.events as events

from umredcap.project import Project

from typing import List


@pytest.fixture
def handlers() -> events.arm_handler:
    credentials: creds.creds = creds.creds()
    ah: events.arm_handler = events.arm_handler(credentials)

    return ah


def test_export_arms(handlers):
    ah = handlers

    arms: pd.DataFrame = ah.export_arms()

    assert arms.shape[0] != 0


def test__get_num_arms(handlers):
    ah = handlers

    n_arms: int = ah._get_num_arms()
    assert n_arms > 0


def test__generate_arms_list(handlers):
    ah = handlers

    # if blank it should produce an range array from 1 to max arms
    max_arms: int = ah._get_num_arms()
    arms_list: List[int] = ah._generate_arms_list()

    assert max(arms_list) == max_arms

    # Should simply return the list it is given otherwise
    input: List[int] = [4, 5, 6, 7]
    output: List[int] = ah._generate_arms_list(input)

    assert input == output


def test_get_event_names(handlers):

    main_project: Project = Project()
    expected: List[str] = [
            '20172018_arm_4',
            '20172018_arm_5',
            '20182019_arm_4',
            '20182019_arm_5',
            ]
    arms: List[int] = [4, 5]
    prev_years = 2
    output: List[str] = main_project.get_event_names(
            arms,
            previous_n_years=prev_years
            )

    assert output == expected
