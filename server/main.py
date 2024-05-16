from cli import Cli
# from server import Server


def main():

    cli = Cli(pi_ip="127.0.0.1", pi_port="5000")
    cli.run()
    # controller.start_server()


if __name__ == "__main__":
    main()
