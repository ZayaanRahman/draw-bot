import time


class Controller:

    # constructor
    def __init__(self):

        # mapping of command name to function
        self.commands = {
            "status": self.status,
            "add": self.add,
            "end": self.end,
            "exit": self.exit
        }

        self.is_started = False
        self.end_flag = False
        
        # history of bot commands sent to the 
        self.history = []

    # start the cli
    def start(self):

        while not self.end_flag:
            self.process_input(input("draw-bot> "))

    # --CLI COMMANDS-----------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------------------------

    # get current robot status
    def status(self, args):
        print(args)

    # add a point or points to robot queue
    # to add 3 points, type args like this: a,b c,d f,g
    def add(self, args):
        print(args)

    # end robot operation
    def end(self, args):
        print(args)

    # exit controller, ending robot operation and controller
    def exit(self, args):
        self.end(args)
        self.end_flag = True

    # --HELPER FUNCTIONS-------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------------------------

    # interpret user input
    def process_input(self, input):

        arg_list = input.split(" ")
        command = arg_list[0].strip()

        if not command in self.commands:
            print("invalid command")
        else:
            self.commands[command](" ".join(arg_list[1:]))
