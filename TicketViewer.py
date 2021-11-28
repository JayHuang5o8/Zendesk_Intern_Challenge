import subprocess
import json


class TicketViewer:
    def __init__(self):
        pass

    # ready to define other behaviors

    def login(self,  domain, username, password):
        '''
        post the login info into zendesk api and check return status
        Return:
            int: the number of tickets it has
            -1: failed
        '''
        # use str() to avoid unsafe input
        self.domain = str(domain)
        self.username = str(username)
        self.password = str(password)
        cmd = "curl https://{0}.zendesk.com/api/v2/tickets/count.json -u {1}:{2}".format(
            domain, username, password)
        # not deal with error situation
        ret = subprocess.run(cmd, shell=True, capture_output=True)
        # if res.returncode == 0:
        res = json.loads(ret.stdout)
        if 'error' in res:
            return -1
        else:
            if 'count' in res and 'value' in res.get('count'):
                return res.get('count').get('value')
            # other wrong
            return -1

    # 0. need user to provide workspace domain, username and password
    # 1. fetch API to get tickets
    # 2. during the fetching process, handle the API unavaliable situation

    def fetch(self) -> list:
        '''
        Fetching tickets from ticket API. If API is not avaliable, return empty list
        Return:
            The list of tickets. If error, return empty list
        '''
        try:
            # fetching
            pass
        except:
            return []

    # 3. need to display

    def get_API(self) -> str:
        '''
        eturn the ticket API
        '''
        pass

    def set_APT(self, api: str) -> int:
        '''
        change the ticket api
        Return:
            1: success
            0: failed
        '''
        pass
