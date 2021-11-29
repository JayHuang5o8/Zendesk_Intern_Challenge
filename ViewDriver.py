from TicketViewer import TicketViewer
import getpass
# The driver to use the ticket viewer
# 1. Displays a friendly error message if the API is unavailable or the response is invalid.
# 2. Tells the user something is wrong if there is a program error.


class commandLineDisplay:
    def __init__(self):
        print("Welcome ot the Zendesk ticket viewer!")
        self.tv = TicketViewer()
        pass

    def start(self):
        '''
        The main driver to start the command line tool
        '''
        failed_cnt = 0
        while True:
            self.domain = input("Please provide your subdomain: ")
            self.username = input("Please provide your login email address: ")
            self.password = getpass.getpass(
                "Please provide your login password: ")
            # TODO failed situation handle
            cnt = self.tv.login(self.domain, self.username, self.password)
            print("")
            if cnt == -1:
                failed_cnt += 1
                print("Sorry, your provided credentials do not in our records.")
                if failed_cnt > 2:
                    print(
                        "Please sign up first or verify your credentials, then try again.")
                    exit()
                print(
                    "Please try again (failed_times : {0})\n".format(failed_cnt))
            if cnt >= 0:
                print("Welcome to {0}!".format(self.domain))
                print("Currently you have {0} tickets.".format(cnt))
                break

        # now the user has successful login
        while True:
            cmd = input("Type 'menu' to view options or 'quit' to exit:\n")
            if cmd != 'menu' and cmd != 'quit':
                continue
            break

        if cmd == 'menu':
            self.menu()
        print("Thanks for using the viewer. Goodbye.")
        exit()

    def menu(self):
        PROMPT = "\n\
        Select view options:\n\
            * Press 1 to view all tickets\n\
            * Press 2 to view a particular\n\
            * Type 'quit' to exit\n"
        while True:
            cmd = input(PROMPT)
            if cmd == 1:
                # TODO display each 25 tickets
                pass
            elif cmd == 2:

                pass
            elif cmd == 'quit':
                return
            else:
                print("Your input is invalid, please re-select.")

    def display_header(self):
        '''
        Set the output format for displaying ticket
        ticket id, status, subject, how long, due_at, assignee_id
        '''
        HEADER = "{0:<10}  {1:<10}  {2:<25}  {3:<20}  {4:<20}  {5:<15}\n".format(
            "Ticket_id", "Status", "Ticket_subject", "Created_date", "Due_at", "assignee_id")
        return HEADER

    def transform(self, ticket: dict):
        '''
        transform a signle ticket to a standard output format
        '''
        res = "{0:<10}  {1:<10}  {2:<25}  {3:<20}  {4:<20}  {5:<15}\n".format(
            ticket.get('id'), ticket.get('status'), ticket.get('subject')[:25],
            str(ticket.get('created_at')), str(ticket.get('due_at')), str(ticket.get('assignee_id')))
        return res

    def display_signle_ticket(self, ticket_id: int):
        '''
        Displaying a signle ticket according to output format
        '''
        ticket = self.tv.fetch_signle_ticket(ticket_id)
        if ticket:
            res = ''
            res += self.display_header()
            res += self.transform(ticket)
            return res
        else:
            print("Ticket id {0} does not exit.".format(ticket_id))

    def display_range_tickets(self, start: int, end: int):
        # for a range of tickets, max range is 25 tickets
        pass


        # first check count.json to see how many tickets it has, then select ticket range
if __name__ == "__main__":
    ctl = commandLineDisplay()
    ctl.start()
