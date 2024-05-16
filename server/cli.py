from controller import Controller

class Cli:
    
    def __init__(self, pi_ip, pi_port):
        self.controller = Controller(pi_ip, pi_port)
        
    def run(self):
        print("\nWelcome 🤖!")
        print("Type \"help\" for a list of commands.\n")
        while not self.controller.end_signal:
            output = self.process_input(input("[🤖?] << "))
            print("[🤖!] >> " + output + "\n")
        
    # interpret user input
    def process_input(self, input):

        arg_list = input.split(" ")
        command = arg_list[0].strip()

        if not command in self.controller.commands:
            return "invalid command"
        else:
            return self.controller.commands[command](arg_list[1:])
        