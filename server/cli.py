from controller import Controller


class Cli(Controller):

    def __init__(self, pi_ip, pi_port):

        super().__init__(pi_ip, pi_port)
        # mapping of command name to function
        self.commands = {
            "help": self.help,
            "status": self.status,
            "add": self.add,
            "start": self.start,
            "end": self.end,
            "exit": self.exit
        }

    def run(self):
        print("\nWelcome 🤖!")
        print("Type \"help\" for a list of commands.\n")
        while not self.end_signal:
            output = self.process_input(input("[🤖?] << "))
            print("[🤖!] >> " + output + "\n")

    # interpret user input
    def process_input(self, input):

        arg_list = input.split(" ")
        command = arg_list[0].strip()

        if not command in self.commands:
            return "invalid command"
        else:
            return self.commands[command](arg_list[1:])

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

    def status(self, args):

        # parse
        state_dict = super().status()
        output = f"robot state at {state_dict["time"]}:\n"
        output += "=================================\n"
        output += f"status: {state_dict["status"]}\n"
        output += f"position: {state_dict["position"]}\n"
        output += f"visited: {state_dict["visited"]}\n"
        output += f"to visit: {state_dict["to visit"]}\n"
        output += "================================="
        return output

    # to add 3 points, type args like this: a,b c,d f,g
    def add(self, args):

        new_pts = []

        for point in args:
            arr = point.split(",")
            if not len(arr) == 2:
                return {"error": "incorrect format, do \"a,b c,d e,f\" for points"}

            x = self.float_conv(arr[0])
            y = self.float_conv(arr[1])

            if x == None or y == None:
                return {"error": "incorrect format, do \"a,b c,d e,f\" for points"}

            new_pts.append([x, y])

        new_queue = super().add(new_pts)["queue"]
        tuple_q = []
        for item in new_queue:
            tuple_q.append(tuple(item))
        return f"updated queue: {tuple_q}"

    def start(self, args):
        return super().start()["message"]

    def end(self, args):
        return super().end()["message"]

    # exit controller, ending robot operation and controller

    def exit(self, args):
        self.end_signal = True
        return "exiting..👋"
