
from robot import Robot
import time


def main():
    robot = Robot()

    robot.start_logger(period=5)
    robot.listen(port=3000)
    # robot.load_points(
    #     [(0, 1), (1, 1), (-1, 2), (3, -2), (3, 1)])

    robot.run(duration=15)
    time.sleep(12)
    print("====== END TEST ===================================================================================")


if __name__ == "__main__":
    main()
