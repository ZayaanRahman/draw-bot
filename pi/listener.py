import threading
from flask import Flask, request

from robot_state import RobotState

# class to abstract the logic of listening to the server for new points
class Listener:
    # constructor
    def __init__(self, state, port):
        self.app = Flask(__name__)
        self.state = state
        self.port = None # for reporting
        self.setup()

    # defines flask endpoints for robot
    def setup(self):

        @self.app.route('/get_status', methods=['GET'])
        def get_status(self):
            return {"status": str(self.state)}

        @self.app.route('/add_points', methods=['POST'])
        def add_points(self):
            points = request.json["points"]

            with self.state.q_lock:
                for point in points:
                    self.state.queue.append(point)
                    
        @self.app.route('/start_run', methods=['POST'])
        def start_run(self):
            # set start_flag to True
            print("not implemented")

        @self.app.route('/end_run', methods=['POST'])
        def end_run(self):
            with self.state.ef_lock:
                self.state.end_flag = True

    # starts thread to listen for points or end flag at port
    def listen(self, port):
        self.port = port
        listen_thread = threading.Thread(target=self.app.run, kwargs={
                                         'port': port}, daemon=True)
        listen_thread.start()
