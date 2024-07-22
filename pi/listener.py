import time
import threading
from flask import Flask, request, jsonify
from flask_cors import CORS

from robot_state import RobotState

# class to abstract the logic of listening to the server for new points


class Listener:
    # constructor
    def __init__(self, state, port):
        self.app = Flask(__name__)
        CORS(self.app)
        self.state = state
        self.port = None  # for reporting
        self.activate_time = None
        self.setup()

    # defines flask endpoints for robot
    def setup(self):

        @self.app.route('/ping', methods=['GET'])
        def ping():
            return jsonify(self.state.to_dict())

        @self.app.route('/get_status', methods=['GET'])
        def get_status():
            return jsonify(self.state.to_dict())

        @self.app.route('/add_points', methods=['PUT'])
        def add_points():
            points = request.json["points"]

            for point in points:
                # once point class made, construct point from lists
                self.state.append_to_queue(tuple(point))
            return jsonify({"queue": list(self.state.get_queue())})

        @self.app.route('/start_run', methods=['POST'])
        def start_run():
            self.state.set_run_flag(True)
            self.state.set_start_time(time.strftime('%H:%M:%S'))
            return jsonify({"message": f"run started at {self.state.get_start_time()}"})

        @self.app.route('/end_run', methods=['POST'])
        def end_run():
            self.state.set_run_flag(False)
            self.state.set_end_time(time.strftime('%H:%M:%S'))
            return jsonify({"message": f"run ended at {self.state.get_end_time()}"})

    # starts thread to listen for points or end flag at port
    def listen(self, port):
        self.port = port
        listen_thread = threading.Thread(target=self.app.run, kwargs={
                                         'port': port}, daemon=True)
        listen_thread.start()
        self.activate_time = time.strftime('%H:%M:%S')
