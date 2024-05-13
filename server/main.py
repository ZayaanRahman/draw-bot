from controller import Controller


def main():

    controller = Controller(pi_ip="127.0.0.1", pi_port="5000")
    controller.run()

if __name__ == "__main__":
    main()
