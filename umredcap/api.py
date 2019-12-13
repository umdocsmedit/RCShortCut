import requests

from umredcap.creds import creds


class api:

    def __init__(self, my_creds: creds):
        self.creds = my_creds

    def resolve_project(self, options: dict) -> dict:
        if 'project' not in options:
            return options

        project_name = options['project']
        credentials = self.creds.load()
        options['token'] = credentials[project_name]
        del options['project']

        return options

    def request(self, options: dict) -> requests.Response:
        options = self.resolve_project(options)
        return requests.post('https://redcap.miami.edu/api/', options)
