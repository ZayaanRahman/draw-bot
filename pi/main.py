
from robot import Robot
import time


def main():

    print("\n====== START TEST =================================================================================\n")
    robot = Robot()

    robot.listen(port=5000)
    # robot.start_file_logger(5)
    # run indefinitely
    # remember, both enable() and run_flag = True are needed for the robot to run
    robot.enable(duration=None)
    print("\n====== END TEST ===================================================================================\n")


if __name__ == "__main__":
    main()
