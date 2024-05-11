import threading
from flask import Flask, request, jsonify

# class to abstract the logic of listening to the server for new points
class Listener:

    def __init__(self, queue, end_flag, port=3000):
        self.app = Flask(__name__)
        
        self.port = port
        self.queue = queue
        self.end_flag = end_flag
        
        self.setup()

    def setup(self):
        
        @self.app.route('/points', methods=['POST'])
        def get_points(self):
            points = request.json["points"]
            
            for point in points:
                self.queue.put(point)
        
        @self.app.route('/end', methods=['POST'])
        def end_run(self):
            end_flag = True
            
    def listen(self):
        