import requests
import umredcap.creds as creds


def resolve_project(options: dict) -> dict:
    if 'project' not in options:
        return options

    project_name = options['project']
    credentials = creds.load()
    options['token'] = credentials[project_name]
    del options['project']

    return options


def request(options: dict) -> requests.Response:
    options = resolve_project(options)
    return requests.post('https://redcap.miami.edu/api/', options)
