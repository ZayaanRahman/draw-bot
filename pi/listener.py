import threading
from flask import Flask, request, jsonify

from robot_state import RobotState

# class to abstract the logic of listening to the server for new points


class Listener:
    # constructor
    def __init__(self, state, port):
        self.app = Flask(__name__)
        self.state = state
        self.port = None  # for reporting
        self.setup()

    # defines flask endpoints for robot
    def setup(self):

        @self.app.route('/get_status', methods=['GET'])
        def get_status():
            return jsonify({"status": str(self.state)})

        @self.app.route('/add_points', methods=['PUT'])
        def add_points():
            points = request.json["points"]

            with self.state.q_lock:
                for point in points:
                    self.state.queue.append(point)
                new_q = self.state.queue
            return jsonify({"queue": list(new_q)})

        @self.app.route('/start_run', methods=['POST'])
        def start_run():
            with self.state.sf_lock:
                self.state.start_flag = True
            return jsonify({"message": "Run started"})

        @self.app.route('/end_run', methods=['POST'])
        def end_run():
            with self.state.ef_lock:
                self.state.end_flag = True
            return jsonify({"message": "Run ended"})

    # starts thread to listen for points or end flag at port
    def listen(self, port):
        self.port = port
        listen_thread = threading.Thread(target=self.app.run, kwargs={
                                         'port': port}, daemon=True)
        listen_thread.start()
