from collections import deque
import threading
import time

# class storing robot state (to be passed to listeners)


class RobotState:
    # constructor
    def __init__(self):
        self.position = (0, 0)
        self.history = []
        self.queue = deque()

        self.start_time = None  # set ONLY when run() is called
        self.end_time = None  # set ONLY when run() ends

        self.start_flag = False  # implement start flag functionality in run function
        self.end_flag = False

        # mutex for queue
        self.q_lock = threading.Lock()

        # mutex for start time
        self.st_lock = threading.Lock()

        # mutex for end time
        self.et_lock = threading.Lock()

        # mutex for end_flag
        self.ef_lock = threading.Lock()

        # mutex for start_flag
        self.sf_lock = threading.Lock()

    # convert state to string
    def __str__(self):

        output = f"robot state at {time.strftime("%H:%M:%S")}:\n"
        output += "=================================\n"

        with self.st_lock:
            s_time = self.start_time

        if s_time == None:
            output += "status: not started yet\n"
        elif not self.end_flag:
            output += f"status: started at {s_time}\n"
        else:
            with self.et_lock:
                output += f"status: ended at {self.end_time}\n"

        output += f"position: {self.position}\n"
        output += f"visited: {self.history}\n"
        with self.q_lock:
            output += f"to visit: {list(self.queue)}\n"

        output += "================================="
        return output

    # print state data every period seconds, for use in a robot thread
    def print_cts(self, period):
        while True:  # continue even after run ends
            print(self)
            time.sleep(period)
