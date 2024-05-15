from controller import Controller


def main():

    Controller(pi_ip="127.0.0.1", pi_port="5000").run()

if __name__ == "__main__":
    main()
