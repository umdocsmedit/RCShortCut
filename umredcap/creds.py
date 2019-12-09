import json


def load(file='creds.json'):
    return json.loads(open(file).read())
