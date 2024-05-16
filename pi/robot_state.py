from collections import deque
import threading
import time
import json

# class storing robot state (to be passed to listeners)
class RobotState:
    # constructor
    def __init__(self):
        self.position = (0, 0)
        self.history = []
        self.queue = deque()

        self.start_time = None  # set ONLY when run() is called
        self.end_time = None  # set ONLY when run() ends

        self.run_flag = False

        # WILL BE REFACTORED TO RUN FLAG
        self.start_flag = False  # implement start flag functionality in run function
        self.end_flag = False

        # mutex for position
        self.pos_lock = threading.Lock()

        # mutex for history
        self.his_lock = threading.Lock()

        # mutex for queue
        self.q_lock = threading.Lock()

        # mutex for latest start time
        self.st_lock = threading.Lock()

        # mutex for latest end time
        self.et_lock = threading.Lock()

        # mutex for run_flag
        self.rf_lock = threading.Lock()

        # mutex for start_flag
        self.sf_lock = threading.Lock()

        # mutex for end_flag
        self.ef_lock = threading.Lock()

    def get_position(self):
        with self.pos_lock:
            return self.position

    def set_position(self, new_pos):
        with self.pos_lock:
            self.position = new_pos

    # getter and setter for history
    def get_history(self):
        with self.his_lock:
            return self.history

    def set_history(self, new_hist):
        with self.his_lock:
            self.history = new_hist

    # getter and setter for queue
    def get_queue(self):
        with self.q_lock:
            return self.queue

    def set_queue(self, new_q):
        with self.q_lock:
            self.queue = new_q

    # getter and setter for start time
    def get_start_time(self):
        with self.st_lock:
            return self.start_time

    def set_start_time(self, new_time):
        with self.st_lock:
            self.start_time = new_time

    # getter and setter for end time
    def get_end_time(self):
        with self.et_lock:
            return self.end_time

    def set_end_time(self, new_time):
        with self.et_lock:
            self.end_time = new_time

    # getter and setter for run flag
    def get_run_flag(self):
        with self.rf_lock:
            return self.run_flag

    def set_run_flag(self, new_flag):
        with self.rf_lock:
            self.run_flag = new_flag

    # getter and setter for start flag
    def get_start_flag(self):
        with self.sf_lock:
            return self.start_flag

    def set_start_flag(self, new_flag):
        with self.sf_lock:
            self.start_flag = new_flag

    # getter and setter for end flag
    def get_end_flag(self):
        with self.ef_lock:
            return self.end_flag

    def set_end_flag(self, new_flag):
        with self.ef_lock:
            self.end_flag = new_flag

    # methods to append to history and append/pop/front from queue
    def append_to_history(self, item):
        with self.his_lock:
            self.history.append(item)

    def append_to_queue(self, item):
        with self.q_lock:
            self.queue.append(item)

    def pop_from_queue(self):
        with self.q_lock:
            return self.queue.popleft()

    def front_of_queue(self):
        with self.q_lock:
            return self.queue[0]

    # convert state to string
    def __str__(self):

        output = f"robot state at {time.strftime('%H:%M:%S')}:\n"
        output += "=================================\n"

        if self.get_start_time() == None:
            output += f"status: not started yet\n"
        elif self.get_run_flag() == True:
            output += f"status: running - started at {self.get_start_time()}\n"
        else:
            output += f"status: not running - stopped at {self.get_end_time()}\n"

        output += f"position: {self.get_position()}\n"
        output += f"visited: {self.get_history()}\n"
        output += f"to visit: {list(self.get_queue())}\n"

        output += "================================="
        return output
    
    # convert state to dict for jsonification
    def to_dict(self):
        state = {
            "time": f"{time.strftime('%H:%M:%S')}",
            "status": "not started yet" if self.get_start_time() is None else "running - started at {}".format(self.get_start_time()) if self.get_run_flag() else "not running - stopped at {}".format(self.get_end_time()),
            "position": self.get_position(),
            "visited": self.get_history(),
            "to visit": list(self.get_queue())
        }
        return state

    # print state data every period seconds, for use in a robot thread
    def print_cts(self, period):
        while True:  # continue even after run ends
            print(self)
            time.sleep(period)
