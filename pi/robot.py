import time
import threading
import copy

from robot_state import RobotState
from listener import Listener

# main class dictating robot operations


class Robot:

    # --INTERFACE FOR ROBOT----------------------------------------------------------------------------
    # -------------------------------------------------------------------------------------------------

    # constructor
    def __init__(self):
        self.state = RobotState()
        self.listener = Listener(self.state, 3000)

    # start a thread to print the robot's state every period seconds
    def start_print_logger(self, period):
        report_thread = threading.Thread(
            target=self.state.log_print, args=[period], daemon=True)
        report_thread.start()
    
    # start a thread to print the robot's state every period seconds
    def start_file_logger(self, period):
        report_thread = threading.Thread(
            target=self.state.log_txt, args=[period], daemon=True)
        report_thread.start()

    # method to manually load points (2-tuples) into queue
    def load_points(self, points):
        with self.state.q_lock:
            for p in points:
                self.state.queue.append(p)

    # start listening thread
    def listen(self, port):
        self.listener.listen(port)

    # Enables running for duration, or infinitely if duration is none
    # Runs when run_flag is true
    # IMPORTANT: as of now, robot will finish moving to a point even of run flag is set to false or duration ends
    def enable(self, duration=None):

        if duration is not None:
            enable_limit = time.time() + duration

        while duration is None or time.time() <= enable_limit:

            # loop while running
            while self.get_run_flag():

                point_count = len(self.get_queue())

                if point_count != 0:
                    target = self.get_queue()[0]
                    self.move(target)
                    self.append_to_history(target)

                    # popping done at end to ensure target stays in queue until finished, and moved to history
                    self.pop_from_queue()

                else:
                    print("nowhere to go\n")
                    time.sleep(3)  # wait 1 sec if no points found

            time.sleep(3)  # check for new flag every second
            print(".\n")

    # --GETTERS AND SETTERS----------------------------------------------------------------------------
    # -------------------------------------------------------------------------------------------------

    # move to target point
    def get_position(self):
        return self.state.get_position()

    def set_position(self, new_pos):
        self.state.set_position(new_pos)

    # getter and setter for history
    def get_history(self):
        return self.state.get_history()

    def set_history(self, new_hist):
        self.state.set_history(new_hist)

    # getter and setter for queue
    def get_queue(self):
        return self.state.get_queue()

    def set_queue(self, new_q):
        self.state.set_queue(new_q)

    # getter and setter for start time
    def get_start_time(self):
        return self.state.get_start_time()

    def set_start_time(self, new_time):
        self.state.set_start_time(new_time)

    # getter and setter for end time
    def get_end_time(self):
        return self.state.get_end_time()

    def set_end_time(self, new_time):
        self.state.set_end_time(new_time)

    # getter and setter for run flag
    def get_run_flag(self):
        return self.state.get_run_flag()

    def set_run_flag(self, new_flag):
        self.state.set_run_flag(new_flag)

    # methods to append to history and append/pop/front from queue
    def append_to_history(self, item):
        self.state.append_to_history(item)

    def append_to_queue(self, item):
        self.state.append_to_queue(item)

    def pop_from_queue(self):
        return self.state.pop_from_queue()
        
    def front_of_queue(self):
        return self.state.front_of_queue()

    # --LOW LEVEL INTERFACE----------------------------------------------------------------------------
    # -------------------------------------------------------------------------------------------------

    # move to target point
    def move(self, target):
        print(f"moving to {target} \n")
        time.sleep(3)  # just for testing
        self.set_position(target)  # not thread safe, edit
