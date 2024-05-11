
from robot import Robot


def main():
    robot = Robot()
    robot.load_points([(0, 1), (1, 1), (-1, 2)])
    robot.run(8)


if __name__ == "__main__":
    main()
