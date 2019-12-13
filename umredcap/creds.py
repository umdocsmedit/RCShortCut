import json


class creds:

    def __init__(self, cred_file='creds.json'):
        self.file = cred_file
        self.url = "https://redcap.miami.edu/api/"

    def load(self):
        return json.loads(open(self.file).read())


configuration = creds()
