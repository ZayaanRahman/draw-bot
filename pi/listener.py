import threading
from flask import Flask, request

# class to abstract the logic of listening to the server for new points


class Listener:

    # constructor
    def __init__(self, state, port):
        self.app = Flask(__name__)

        self.port = port
        self.state = state

        self.setup()

    # defines flask endpoints for robot
    def setup(self):

        @self.app.route('/points', methods=['POST'])
        def get_points(self):
            points = request.json["points"]

            for point in points:
                self.state.queue.put(point)

        @self.app.route('/end', methods=['POST'])
        def end_run(self):
            self.state.end_flag = True

    # starts thread to listen for points or end flag
    def listen(self):
        listen_thread = threading.Thread(target=self.app.run, kwargs={
                                         'port': self.port}, daemon=True)
        listen_thread.start()

        print(f"Listening on port {self.port}\n")
