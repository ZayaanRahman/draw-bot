import time
import requests
import json

# class for CLI
class Controller:

    # constructor
    def __init__(self, pi_ip, pi_port):

        self.pi_address = "http://" + pi_ip + ":" + pi_port + "/"

        # mapping of command name to function
        self.commands = {
            "help": self.help,
            "status": self.status,
            "add": self.add,
            "start": self.start,
            "end": self.end,
            "exit": self.exit
        }

        self.is_started = False
        self.end_flag = False

        # history of bot commands, not implemented
        self.history = []

    # start the cli
    def run(self):
        print("\nWelcome 🤖!")
        print("Type \"help\" for a list of commands.\n")
        while not self.end_flag:
            print("[🤖!] >> " + self.process_input(input("[🤖?] << ")) + "\n")

    # --CLI COMMANDS-----------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------------------------

    # list commands and functionality
    def help(self, args):
        output = "commands:\n"
        output += "=================================\n"
        output += "help: list commands\n"
        output += "status: view robot state\n"
        output += "add: append points to robot itinerary\n"
        output += "start: start robot movement\n"
        output += "end: end robot movement\n"
        output += "exit: exit controller\n"
        output += "================================="
        return output

    # get current robot status
    def status(self, args):
        # print(self.pi_address+"get_status")
        response = requests.get(self.pi_address + "get_status")
        return response.json()["status"]

    # add a point or points to robot queue
    # to add 3 points, type args like this: a,b c,d f,g
    def add(self, args):

        new_pts = []

        for point in args:
            arr = point.split(",")
            if not len(arr) == 2:
                return "incorrect format, do \"a,b c,d e,f\" for points"

            x = self.float_conv(arr[0])
            y = self.float_conv(arr[1])

            if x == None or y == None:
                return "incorrect format, do \"a,b c,d e,f\" for points"

            new_pts.append([x, y])

        headers = {'Content-Type': 'application/json'}
        json_data = json.dumps({"points": new_pts})

        response = requests.put(
            self.pi_address + "add_points", data=json_data, headers=headers)
        return "updated queue: " + str(response.json()["queue"])

    # start robot operation

    def start(self, args):
        response = requests.post(self.pi_address + "start_run")
        return response.json()["message"]

    # end robot operation
    def end(self, args):
        response = requests.post(self.pi_address + "end_run")
        return response.json()["message"]

    # exit controller, ending robot operation and controller
    def exit(self, args):
        self.end_flag = True
        return "exiting..👋"

    # --HELPER FUNCTIONS-------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------------------------

    # interpret user input
    def process_input(self, input):

        arg_list = input.split(" ")
        command = arg_list[0].strip()

        if not command in self.commands:
            return "invalid command"
        else:
            return self.commands[command](arg_list[1:])

    def float_conv(self, str):
        try:
            f = float(str)
            return f
        except ValueError:
            return None