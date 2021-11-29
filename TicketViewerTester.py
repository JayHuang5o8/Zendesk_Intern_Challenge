import unittest
from TicketViewer import TicketViewer
import getpass


class TicketViewerTester(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.tv = TicketViewer()
        print("For successful testing, please provide a correct credential")
        self.domain = input("Please provide a correct subdomain: ")
        self.username = input("Please provide a correct login email address: ")
        self.password = getpass.getpass(
            "Please provide a correct login password: ")

    def test_execute_fail_1(self):
        '''
        wrong credentials
        '''
        wrong_credentials_cmd = "curl https://{0}.zendesk.com/api/v2/tickets/count.json -u {1}:{2}".format(
            'test', 'test', 'test')
        self.assertTrue('error' in self.tv.execute_cmd(wrong_credentials_cmd))

    def test_execute_fail_2(self):
        '''
        invalid api
        '''
        invalid_api = "curl https://{0}.zendesk.com/api/tickets/count.json -u {1}:{2}".format(
            self.domain, self.username, self.password)
        self.assertEqual(self.tv.execute_cmd(invalid_api), 'error')

    def test_execute_success(self):
        correct_cmd = "curl https://{0}.zendesk.com/api/v2/tickets/count.json -u {1}:{2}".format(
            self.domain, self.username, self.password)
        self.assertIsInstance(self.tv.execute_cmd(correct_cmd), dict)

    def test_login_fail_1(self):
        '''
        wrong credentials
        '''
        self.assertEqual(self.tv.login('test', 'test', 'test'), -1)

    def test_login_success(self):
        self.assertTrue(self.tv.login(
            self.domain, self.username, self.password) >= 0)

    def test_fetch_range_ticket_fail_1(self):
        '''
        wrong credentials
        '''
        res = self.tv.fetch_range_tickets('test', 'test', 'test')
        self.assertEqual(res[0], 'error')

    def test_fetch_range_ticket_success(self):
        res = self.tv.fetch_range_tickets(
            self.domain, self.username, self.password)
        self.assertTrue(len(res) >= 0)

    def test_fetch_single_ticket_fail_1(self):
        '''
        ticket id is not valid
        '''
        self.assertEqual(self.tv.fetch_signle_ticket(
            self.domain, self.username, self.password, -1), None)

    def test_fetch_single_ticket_success(self):
        tickets = self.tv.fetch_range_tickets(
            self.domain, self.username, self.password)
        valid_id = tickets[0].get('id')
        res = self.tv.fetch_signle_ticket(
            self.domain, self.username, self.password, valid_id)
        self.assertIsInstance(res, dict)


if __name__ == '__main__':
    unittest.main()
