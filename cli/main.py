from cli import Cli
# from server import Server

# pi="192.168.1.89"
# localhost="127.0.0.1"


def main():

    cli = Cli(pi_ip="10.0.0.28", pi_port="5000")
    cli.run()

    # server = Server(pi_ip="", pi_port="5000")
    # server.run(port=3000)


if __name__ == "__main__":
    main()
