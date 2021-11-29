from TicketViewer import TicketViewer
import getpass
import math
from dateutil import parser
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
            self.ticket_cnt = self.tv.login(
                self.domain, self.username, self.password)
            print("")
            if self.ticket_cnt == -1:
                failed_cnt += 1
                print("Sorry, your provided credentials do not match our records.")
                if failed_cnt > 2:
                    print(
                        "Please sign up first or verify your credentials, then try again.")
                    exit()
                print(
                    "Please try again (failed_times : {0})\n".format(failed_cnt))
            if self.ticket_cnt >= 0:
                print("Welcome to {0}!".format(self.domain))
                print("Currently you have {0} tickets.".format(
                    self.ticket_cnt))
                break

        # now the user has successful login
        while True:
            cmd = input(" * Type 'menu' to view options or 'quit' to exit:\n")
            if cmd != 'menu' and cmd != 'quit':
                continue
            break

        if cmd == 'menu':
            self.menu()
        print("Thanks for using the viewer. Goodbye.")
        exit()

    def menu(self):
        '''
        The main menu of the ticket viewer. User can choose:
            1. view all tickets
            2. view a particular ticket
            3. exit program
        '''
        PROMPT = "\nSelect view options:\n\
    * Press 1 to view all tickets\n\
    * Press 2 to view a particular\n\
    * Type 'quit' to exit\n"
        while True:
            cmd = input(PROMPT)
            if cmd == '1':
                self.display_all_tickets()
            elif cmd == '2':
                while True:
                    ticket_id = input("Enter ticket number:\n")
                    if ticket_id.isdigit():
                        break
                    print('Please input a number')
                    ticket_id = int(ticket_id)
                self.display_signle_ticket(ticket_id)
            elif cmd == 'quit':
                return
            else:
                print("Your input is invalid, please re-select.")

    def display_all_tickets(self):
        '''
        Display all tickets. For each page, only display 25 tickets.
        page */*, page up, page down, menu
        '''
        all_tickets = self.tv.fetch_range_tickets()
        if all_tickets[0] == 'error':
            print("Cannot fetch your tickets, error meeage is", all_tickets[1])
            return
        if len(all_tickets) > 25:
            # it needs to be spilt into different pages
            total_page = math.ceil(len(all_tickets)/25)
            cur_page = 1
            while cur_page <= total_page:
                self.display_range_tickets(
                    all_tickets, start=25*(cur_page-1), end=25*cur_page)
                cmd = self.display_page_selection(cur_page, total_page)
                if cmd == '1':
                    cur_page -= 1
                elif cmd == '2':
                    cur_page += 1
                else:
                    break
        else:
            # all tickets can be shown in one page
            self.display_range_tickets(
                all_tickets, start=0, end=len(all_tickets))

    def display_range_tickets(self, tickets: list, start: int, end: int):
        '''
        Display a range of tickets, which from start to end
        '''
        res = self.display_header()
        for ticket in tickets[start:end]:
            res += self.content_transform(ticket)
        res += "="*120
        print(res)

    def display_header(self):
        '''
        Set the output format for displaying ticket
        ticket id, status, subject, how long, due_at, assignee_id
        '''
        HEADER = "="*120 + "\n"
        HEADER += "{0:<10}  {1:<10}  {2:<25}  {3:15}  {4:<15}  {5:15}  {6:<15}\n".format(
            "Ticket_id", "Status", "Ticket_subject", "Created_date", "Due_at", "Priority", "assignee_id")
        return HEADER

    def datetime_transform(self, time):
        '''
        import an ISO 8601 format datetime, export a %Y-%M-%D datetime string 
        '''
        if time is None:
            return "None"
        time = parser.parse(time)
        return time.strftime('%Y-%m-%d')

    def content_transform(self, ticket: dict):
        '''
        transform a signle ticket to a standard output format
        '''
        res = "{0:<10}  {1:<10}  {2:<25}  {3:15}  {4:<15}  {5:15}  {6:<15}\n".format(
            ticket.get('id'), ticket.get('status'), ticket.get('subject')[:25],
            self.datetime_transform(ticket.get('created_at')),
            self.datetime_transform(ticket.get('due_at')),
            str(ticket.get('priority')),
            str(ticket.get('assignee_id')))
        return res

    def display_page_selection(self, cur_page: int, total_page: int):
        '''
        After diplaying a page of tickets, prompt page operation 
        '''
        # displaying the page location
        OPERATION = "Pages: {0}/{1}\n".format(cur_page, total_page)
        OPERATION += " * "
        # according to the page location, print different operations
        if cur_page != 1:
            OPERATION += "Press 1 to last page. "
        if cur_page != total_page:
            OPERATION += "Press 2 to next page. "
        OPERATION += "Type 'menu' to main menu.\n"
        cmd = input(OPERATION)
        # check invalid input
        if cmd not in ['1', '2', 'menu'] or\
            (cur_page == 1 and cmd == '1') or\
                (cur_page == total_page and cmd == '2'):
            print("Please type valid input.")
            return self.display_page_selection(cur_page, total_page)
        return cmd

    def display_signle_ticket(self, ticket_id: int):
        '''
        Displaying a signle ticket according to output format
        '''
        ticket = self.tv.fetch_signle_ticket(ticket_id)
        if ticket:
            res = self.display_detailed_header()
            res += self.detailed_content_transform(ticket)
            res += "="*120
            print(res)
        else:
            print("Ticket id {0} does not exit. \
                Please enter an existing ticket id".format(ticket_id))

    def display_detailed_header(self):
        '''
        Display a more detailed information of a ticket. During the selection, user already
        know the ticket id, the status, and the assignee, so ignore these information
        '''
        HEADER = "="*120 + "\n"
        HEADER += " {0:<30}  {1:30}  {2:<10}  {3:<15}  {4:<15}  {5:<15}  {6:<20}\n".format(
            "Ticket_subject", "Description", "Type", "Priority", "Due Date", "Organization_id", "Recipient")
        return HEADER

    def detailed_content_transform(self, ticket: dict):
        '''
        transform a signle ticket to a detailed output format
        '''
        res = " {0:<30}  {1:30}  {2:<10}  {3:<15}  {4:<15}  {5:<15}  {6:<20}\n".format(
            ticket.get('subject')[:30],
            str(ticket.get('description'))[:30],
            str(ticket.get('type')),
            str(ticket.get('priority')),
            self.datetime_transform(ticket.get('due_at')),
            str(ticket.get('organization_id')),
            str(ticket.get('recipient')))
        return res


if __name__ == "__main__":
    ctl = commandLineDisplay()
    ctl.start()
