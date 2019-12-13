import math
import logging
import requests

import pandas as pd  # type: ignore

from umredcap.creds import creds
from umredcap.api import api

from typing import List


LOGGER = logging.getLogger('records')


class record_handler:

    def __init__(self, my_creds: creds):
        self.api = api(my_creds)

    def export_event_records(
            self,
            project='new_redcap',
            events: List[str] = []
            ) -> pd.DataFrame:

        data = pd.DataFrame()

        request_data = {
                'project': project,
                'content': 'record',
                'format': 'json',
                'type': 'flat',
                'rawOrLabel': 'raw',
                'rawOrLabelHeaders': 'raw',
                'exportCheckboxLabel': 'false',
                'exportSurveyFields': 'false',
                'exportDataAcessGroups': 'false',
                'returnFormat': 'json'
                }

        n_events_per_request: int = 5
        n_requests = math.ceil(len(events) / n_events_per_request)

        for request_set in range(n_requests):
            LOGGER.debug(f'Processing request {request_set} of {n_requests-1}')

            first_event_index: int = request_set * n_events_per_request
            last_event_index: int = first_event_index + n_events_per_request
            request_events: List[str] = events[
                    first_event_index:last_event_index]

            for index, event in enumerate(request_events):
                key = f'events[{index}]'
                value = event
                request_data[key] = value

            response: requests.Response = self.api.request(request_data)
            response_data: pd.DataFrame = pd.read_json(
                    response.text, convert_dates=False
                    )
            data = data.append(response_data, ignore_index=True)

        return data
