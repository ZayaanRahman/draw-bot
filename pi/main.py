
from robot import Robot
import time


def main():

    print("\n====== START TEST =================================================================================\n")
    robot = Robot()
    robot.start_logger(period=5)
    robot.load_points([(0, 0), (1, 1), (2, 2), (3, 3)])
    robot.listen(port=3000)
    # run for 30 sec or until end flag
    # remember, both enable() and start_flag = True are needed for the robot to run
    robot.enable(duration=30)
    time.sleep(3)
    print("\n====== END TEST ===================================================================================\n")


if __name__ == "__main__":
    main()
