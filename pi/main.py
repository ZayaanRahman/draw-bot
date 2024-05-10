
import robot


def main():
    r = robot.Robot()
    r.load_points([(0, 1), (1, 1), (-1, 2)])
    r.run(8)


if __name__ == "__main__":
    main()
