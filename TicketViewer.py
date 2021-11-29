import subprocess
import json


class TicketViewer:
    def __init__(self):
        pass

    def execute_cmd(self, cmd: str):
        '''
        The function to handle the curl command. 
        When API is not avaliable, return "error"
        Return:
            curl result
        '''
        ret = subprocess.run(cmd, shell=True, capture_output=True)
        # if res.returncode == 0:
        try:
            # when API is not avaliable, the result is not json format
            res = json.loads(ret.stdout)
        except:
            return 'error'
        return res

    def login(self, domain: str, username: str, password: str):
        '''
        Post the login info into zendesk api and check return status
        Return:
            int: the number of tickets the agent has
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
            # the provided credentials are not valid or the api is not avaliable
            return -1
        else:
            # make sure the returned format has 'value' and 'count' key
            if 'count' in res and 'value' in res.get('count'):
                return res.get('count').get('value')
            # other unknown error sitution, may be the json format is changed
            return -1

    def fetch_signle_ticket(self, ticket_id: int) -> dict:
        '''
        Fetch a signle ticket of particular ticket_id from ticket api
        Args:
            ticket_id: the ticket id of a particular number
        Return:
            the dictionary format of the ticket details;
            None if the ticket is not avalible 
        '''
        cmd = "curl https://{0}.zendesk.com/api/v2/tickets/{3}.json \
            -u {1}:{2}".format(self.domain, self.username, self.password, ticket_id)
        res = self.execute_cmd(cmd)
        if 'error' in res:
            # when ticket id does not exist, api will return error
            return None
        return res.get('ticket')

    def fetch_range_tickets(self) -> list:
        '''
        Fetching all tickets from an agent. 
        According to api document, each curl can only load 100 max 
        tickets per page, which is a limitation of curl api
        Return:
            The list of tickets. 
            If error, return ['error', error message]
        '''
        cmd = "curl https://{0}.zendesk.com/api/v2/tickets.json \
            -u {1}:{2}".format(self.domain, self.username, self.password)
        res = self.execute_cmd(cmd)
        if 'error' in res:
            # when ticket id does not exist, api will return error
            return ['error', res.get('error')]
        return res.get('tickets')
