import time
import requests
import json

# class for CLI


class Controller:

    # constructor
    def __init__(self, pi_ip, pi_port):

        self.pi_address = "http://" + pi_ip + ":" + pi_port + "/"

    # --BASE COMMANDS----------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------------------------

    # get current robot status
    def status(self):
        response = requests.get(self.pi_address + "get_status")
        return response.json()

    # add a point or points to robot queue
    def add(self, new_points):

        headers = {'Content-Type': 'application/json'}
        json_data = json.dumps({"points": new_points})

        response = requests.put(
            self.pi_address + "add_points", data=json_data, headers=headers)
        
        return response.json()

    # start robot operation
    def start(self):
        response = requests.post(self.pi_address + "start_run")
        return response.json()

    # end robot operation
    def end(self):
        response = requests.post(self.pi_address + "end_run")
        return response.json()

    # --HELPER FUNCTIONS-------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------------------------

    def float_conv(self, str):
        try:
            f = float(str)
            return f
        except ValueError:
            return None
