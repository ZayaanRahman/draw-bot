from controller import Controller
from flask import Flask, request, jsonify

# simple class to activate server for web interface
class Server(Controller):

    def __init__(self, pi_ip, pi_port):
        super().__init__(pi_ip, pi_port)
        self.port = None
        self.app = Flask(__name__)

        self.setup()

    def setup(self):

        @self.app.route('/get_status', methods=['GET'])
        def get_status():
            return jsonify(self.status())

        @self.app.route('/add_points', methods=['PUT'])
        def add_points():
            return jsonify(self.add(request.json["points"]))

        @self.app.route('/start_run', methods=['POST'])
        def start_run():
            return jsonify(self.start())

        @self.app.route('/end_run', methods=['POST'])
        def end_run():
            return jsonify(self.end())
        
    def run(self, port):
        self.port = port
        self.app.run(port=port)
