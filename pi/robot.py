import time
import queue


class Robot:

    # constructor, duration in sec
    def __init__(self):
        self.queue = queue.Queue()
        self.history = []
        self.birth_time = time.time()  # for logging
        print(f"robot constructed at {self.birth_time} \n")

    # method to manually load points (pair) into queue
    def load_points(self, points):
        for p in points:
            self.queue.put(p)

    # run the robot
    def run(self, duration=60):

        start_time = time.time()
        print(f"began running at {start_time} \n")
        end_time = start_time + duration

        self.listen(3000)

        while time.time() <= end_time:

            if not self.queue.empty():
                target = self.queue.get()
                self.move(target)
                self.history.append(target)
            else:
                print("nowhere to go\n")
                time.sleep(1)  # wait 1 sec if no points found

        print(f"ended running at {time.time()} \n")

    # listen to server for new points asynchronously, and add them to the points list
    def listen(self, port):
        print(f"listening on port {port} \n")
        # Will have an endpoint to accept points, and another to end execution

    # move to target point
    def move(self, target):
        print(f"moving to {target} \n")
        time.sleep(2)  # just for testing
