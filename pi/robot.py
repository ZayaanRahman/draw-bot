import time
import queue
from listener import Listener

# main class dictating robot operations
class Robot:

    # constructor
    def __init__(self):
        self.position = (0,0)
        self.queue = queue.Queue()
        self.history = []
        
        self.end_flag = False
        
        self.listener = Listener(self.queue, self.end_flag, 3000)
        
        
        self.birth_time = time.time()  # for logging
        print(f"robot constructed at {self.birth_time} \n")

    # method to manually load points (pair) into queue
    def load_points(self, points):
        for p in points:
            self.queue.put(p)

    # run the robot, duration in sec
    def run(self, duration=60):

        start_time = time.time()
        print(f"began running at {start_time} \n")
        end_time = start_time + duration

        self.listener.listen()

        while time.time() <= end_time or self.end_flag:

            if not self.queue.empty():
                target = self.queue.get()
                self.move(target)
                self.history.append(target)
            else:
                print("nowhere to go\n")
                time.sleep(1)  # wait 1 sec if no points found

        print(f"ended running at {time.time()} \n")

    # move to target point
    def move(self, target):
        print(f"moving to {target} \n")
        vector = target - self.position
        time.sleep(2)  # just for testing
