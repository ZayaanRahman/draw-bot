import time
import requests
import json


class Controller:

    # constructor
    def __init__(self, pi_ip, pi_port):

        self.pi_address = "http://" + pi_ip + ":" + pi_port + "/"

        # mapping of command name to function
        self.commands = {
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

        while not self.end_flag:
            self.process_input(input("draw-bot > "))

    # --CLI COMMANDS-----------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------------------------

    # get current robot status
    def status(self, args):
        # print(self.pi_address+"get_status")
        response = requests.get(self.pi_address + "get_status")
        print(response.json()["status"])

    # add a point or points to robot queue
    # to add 3 points, type args like this: a,b c,d f,g
    def add(self, args):

        new_pts = []

        for point in args:
            arr = point.split(",")
            if not len(arr) == 2:
                print("incorrect format, do \"a,b c,d e,f\" for points")
                return
            x = self.float_conv(arr[0])
            y = self.float_conv(arr[1])

            if x == None or y == None:
                print("incorrect format, do \"a,b c,d e,f\" for points")
                return

            new_pts.append([x, y])

        headers = {'Content-Type': 'application/json'}
        json_data = json.dumps({"points": new_pts})

        response = requests.put(
            self.pi_address + "add_points", data=json_data, headers=headers)
        print("updated queue: " + str(response.json()["queue"]))

    # start robot operation

    def start(self, args):
        response = requests.post(self.pi_address + "start_run")
        print(response.json()["message"])

    # end robot operation
    def end(self, args):
        response = requests.post(self.pi_address + "end_run")
        print(response.json()["message"])

    # exit controller, ending robot operation and controller
    def exit(self, args):
        print("exiting...")
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
            self.commands[command](arg_list[1:])

    def float_conv(self, str):
        try:
            f = float(str)
            return f
        except ValueError:
            return None
