import math
import redcap  # type: ignore
import logging
import umredcap

import pandas as pd  # type: ignore

from umredcap.creds import configuration
from typing import List, Any

LOGGER = logging.getLogger("project")


class Project(redcap.Project):

    def __init__(self, project_name: str = 'new_redcap'):
        super().__init__(
                configuration.url,
                configuration.load()[project_name])

    def export_event_records(
            self,
            events: List[str] = [],
            n_events_per_request=5,
            **kwargs) -> Any:

        if len(events) < 1:
            LOGGER.debug("No events listed, getting events")
            events = self.get_event_names()

        data = pd.DataFrame()
        n_events: int = len(events)
        n_requests: int = math.ceil(n_events / n_events_per_request)

        for request_set in range(n_requests):
            LOGGER.debug(f'Processing request {request_set} of {n_requests-1}')
            first_event_index: int = request_set * n_events_per_request
            last_event_index: int = first_event_index + n_events_per_request
            request_events = events[first_event_index:last_event_index]
            LOGGER.debug(f'Events: {request_events}')

            kwargs['events'] = request_events
            response = self.export_records(**kwargs)
            response_data: pd.DataFrame = pd.DataFrame(response)
            LOGGER.debug(f'Obtained {response_data.shape[0]} records')
            data = data.append(response_data, ignore_index=True)
            LOGGER.debug(f'Current Data Size: {data.shape}')

        return data

    def get_event_names(self,
                        arms: List[int] = [],
                        years: List[int] = [],
                        previous_n_years: int = 0) -> List[str]:
        """Returns a list of event names given the arm numbers and either an
        array of academica years (beginning in the fall) or an integer of the
        previous n number of years. If both years, and previous_n_years are
        used, they are merged and uniqued"""
        year_strs = umredcap.events._generate_years_list(
                years, previous_n_years)
        events = []

        for year_str in year_strs:
            for arm in arms:
                event = f'{year_str}_arm_{arm}'
                events.append(event)

        events_df: pd.DataFrame = pd.DataFrame(self.events)
        event_names: List[str] = events_df['unique_event_name'].to_list()
        events = [x for x in events if x in event_names]

        if len(events) < 1:
            events = event_names

        return events
