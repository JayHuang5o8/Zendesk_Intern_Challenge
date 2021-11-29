import subprocess
import json


class TicketViewer:
    def __init__(self):
        pass

    def execute_cmd(self, cmd: str):
        '''
        The function to handle the curl command. In this function, handle exceptions
        Return:
            curl result
        '''
        ret = subprocess.run(cmd, shell=True, capture_output=True)
        # if res.returncode == 0:
        res = json.loads(ret.stdout)
        return res

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

        res = self.execute_cmd(cmd)
        if 'error' in res:
            return -1
        else:
            if 'count' in res and 'value' in res.get('count'):
                return res.get('count').get('value')
            # other wrong
            return -1

    # 1. fetch API to get tickets
    # 2. during the fetching process, handle the API unavaliable situation

    def fetch_signle_ticket(self, ticket_id: int) -> dict:
        cmd = "curl https://{0}.zendesk.com/api/v2/tickets/{3}.json -u {1}:{2}".format(
            self.domain, self.username, self.password, ticket_id)
        res = self.execute_cmd(cmd)
        if 'error' in res:
            return None
        return res

    def fetch_range_tickets(self, start: int, end: int) -> list:
        '''
        Fetching tickets from start id to end id. 
        Return:
            The list of tickets. If error, return empty list
        '''
        try:
            # fetching
            pass
        except:
            return []

    # 3. need to display
