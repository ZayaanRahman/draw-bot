
from robot import Robot


def main():
    robot = Robot()
    print(robot.state)

    robot.load_points([(0, 1), (1, 1), (-1, 2)])
    print(robot.state)

    robot.run(8)
    print(robot.state)


if __name__ == "__main__":
    main()
