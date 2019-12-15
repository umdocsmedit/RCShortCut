import os
import json


class creds:

    def __init__(self, cred_file='creds.json'):
        self.file = cred_file
        self.url = "https://redcap.miami.edu/api/"
        self.envs = self.check_envs()

    def check_envs(self):
        try:
            os.environ['new_redcap']
        except KeyError:
            return False

        return True

    def load(self):
        if self.envs is False:
            return json.loads(open(self.file).read())
        else:
            return {
                    'new_redcap': os.environ['new_redcap'],
                    'test_redcap': os.environ['test_redcap']
                    }


configuration = creds()
