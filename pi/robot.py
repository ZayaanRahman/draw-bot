import time
import threading

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
    def start_logger(self, period):
        report_thread = threading.Thread(
            target=self.state.print_cts, args=[period], daemon=True)
        report_thread.start()

    # method to manually load points (2-tuples) into queue
    def load_points(self, points):
        with self.state.q_lock:
            for p in points:
                self.state.queue.append(p)

    # start listening thread
    def listen(self, port):
        self.listener.listen(port)

    # enable the robot, allowing it to start when a run command is sent
    # if duration is None, run infinitely until end flag is set
    # else, end after duration secs
    def enable(self, duration=None):

        # wait until start flag is set before starting
        while not self.should_start():
            print("not started yet")
            time.sleep(1)  # wait a second before checking for start again

        # set start time once past start block
        with self.state.st_lock:
            self.state.start_time = time.time()

        while not self.should_end(duration):

            with self.state.q_lock:
                point_count = len(self.state.queue)

            if not point_count == 0:
                with self.state.q_lock:
                    target = self.state.queue[0]
                self.move(target)
                self.state.history.append(target)

                # popping done at end to ensure target stays in queue until finished, and moved to history
                with self.state.q_lock:
                    target = self.state.queue.popleft()

            else:
                print("nowhere to go\n")
                time.sleep(2)  # wait 1 sec if no points found

        with self.state.ef_lock:
            self.state.end_flag = True  # for post-run logging and consistency
        with self.state.et_lock:
            self.state.end_time = time.time()

    # --"LOW LEVEL" AND HELPER FUNCTIONS---------------------------------------------------------------
    # -------------------------------------------------------------------------------------------------

    # move to target point
    def move(self, target):
        print(f"moving to {target} \n")
        time.sleep(2)  # just for testing

    # check if robot should start safely
    def should_start(self):
        with self.state.sf_lock:
            sf = self.state.start_flag

        return sf

    # check if robot should end safely
    def should_end(self, duration):

        with self.state.st_lock:
            s_time = self.state.start_time
        with self.state.ef_lock:
            e_flag = self.state.end_flag

        # do demorgans
        return not (not e_flag and (duration == None or time.time() < s_time + duration))
