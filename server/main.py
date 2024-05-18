from cli import Cli
from server import Server
# from server import Server


def main():

    cli = Cli(pi_ip="", pi_port="5000")
    cli.run()
    
    # server = Server(pi_ip="", pi_port="5000")
    # server.run(port=3000)


if __name__ == "__main__":
    main()
