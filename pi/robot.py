import time
from queue import Queue
from copy import copy
from listener import Listener


# class storing robot state (to be passed to listeners)
class RobotState:
    def __init__(self):
        self.position = (0, 0)
        self.queue = Queue()
        self.history = []

        self.start_time = None  # set when run is executed
        self.end_flag = False

    def __str__(self):

        output = ""

        if self.start_time == None:
            output += "not started yet\n"
        else:
            output += f"started at {self.start_time}\n"

        output += f"position: {self.position}\n"
        output += f"visited: {self.history}\n"
        output += f"to visit: {list(self.queue.queue)}\n"

        return output

# main class dictating robot operations


class Robot:

    # constructor
    def __init__(self):
        self.state = RobotState()
        self.listener = Listener(self.state, 3000)

    # method to manually load points (pair) into queue
    def load_points(self, points):
        for p in points:
            self.state.queue.put(p)

    # run the robot, duration in sec
    def run(self, duration=60):

        self.state.start_time = time.time()
        end_time = self.state.start_time + duration

        self.listener.listen()

        while time.time() <= end_time or self.state.end_flag:

            if not self.state.queue.empty():
                target = self.state.queue.get()
                self.move(target)
                self.state.history.append(target)
            else:
                print("nowhere to go\n")
                time.sleep(1)  # wait 1 sec if no points found

        print(f"ended running at {time.time()} \n")

    # move to target point
    def move(self, target):
        print(f"moving to {target} \n")
        time.sleep(1)  # just for testing
