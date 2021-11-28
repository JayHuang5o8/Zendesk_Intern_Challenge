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
                    print("Please sign up first or verify your credentials.")
                    exit()
                print(
                    "Please try again (failed_times : {0})".format(failed_cnt))
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
        pass

        # first check count.json to see how many tickets it has, then select ticket range
if __name__ == "__main__":
    ctl = commandLineDisplay()
    ctl.start()
