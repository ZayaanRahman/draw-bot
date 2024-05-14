
from robot import Robot
import time


def main():

    print("\n====== START TEST =================================================================================\n")
    robot = Robot()
    robot.listen(port=5000)
    # run for 30 sec or until end flag
    # remember, both enable() and start_flag = True are needed for the robot to run
    robot.enable(duration=None)
    print("\n====== END TEST ===================================================================================\n")


if __name__ == "__main__":
    main()
