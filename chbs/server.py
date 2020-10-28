import argparse
import os
import os.path
import random
import select
import socket
import sys

__version__ = "0.2.1"

parser = argparse.ArgumentParser()
parser.add_argument(
    "-v", "--version", help="Print version and exit", action="store_true", default=False
)
parser.add_argument(
    "--root",
    help="File root - a `nouns.txt` and `adjectives.txt` must be found here.",
    default=os.path.dirname(os.path.abspath(__file__)),
)
parser.add_argument(
    "--host",
    help="Host or IP address to listen on",
    default=os.environ.get("HOST", "0.0.0.0"),
)
parser.add_argument(
    "--port", help="Port to listen on", type=int, default=os.environ.get("PORT", 8000)
)
parser.add_argument(
    "--launch",
    choices=("single", "select", "epoll"),
    help="The type of server to run.",
    default="single",
)
parser.add_argument(
    "--one",
    action="store_true",
    default=False,
    help="Only generate a single passphrase on the command line.",
)


class CorrectHorseBatteryStaple:
    def __init__(self, nouns, adjectives):
        self.nouns = [noun.strip() for noun in nouns if noun.strip()]
        self.adjectives = [
            adjective.strip() for adjective in adjectives if adjective.strip()
        ]

    def generate(self):
        return "{} {} {} {}".format(
            random.choice(self.adjectives),
            random.choice(self.nouns),
            random.choice(self.nouns),
            random.choice(self.nouns),
        )


def make_resp(data):
    return f"""\
HTTP/1.1 200 OK
Server: correcthorsebatterystaple/1.0.0
Content-Type: text/plain
Content-Length: {len(data)}

{data}"""


def single_server(host, port, correcthorsebatterystaple):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print(f"Server starting on {host}:{port}")
        sock.bind((host, port))
        sock.listen(10)
        try:
            while True:
                client, addr = sock.accept()
                data = client.recv(4096)  # This should be enough for the HTML header
                client.send(make_resp(correcthorsebatterystaple.generate()).encode())
                client.close()
        except KeyboardInterrupt:
            print("Bye")


def select_server(host, port, correcthorsebatterystaple):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print(f"Server starting on {host}:{port}")
        sock.bind((host, port))
        sock.listen(10)
        try:
            waiting_for_request = [sock]
            waiting_for_response = []
            while True:
                read_list = [sock]
                readable, writable, errored = select.select(
                    waiting_for_request, waiting_for_response, []
                )
                for s in writable:
                    s.send(make_resp(correcthorsebatterystaple.generate()).encode())
                    s.close()
                    waiting_for_response.remove(s)
                for s in readable:
                    if s is sock:
                        client, addr = sock.accept()
                        waiting_for_request.append(client)
                    else:
                        data = s.recv(4096)  # But... really we don't care.
                        # literally any request is going to get back a
                        # correct horse battery staple
                        waiting_for_response.append(s)
                        waiting_for_request.remove(s)
        except KeyboardInterrupt:
            print("Bye")


def epoll_server(host, port, correcthorsebatterystaple):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print(f"Server starting on {host}:{port}")
        sock.bind((host, port))
        sock.listen(10)
        sock.setblocking(0)

        epoll = select.epoll()
        epoll.register(sock.fileno(), select.EPOLLIN)
        try:
            connections = {}
            while True:
                events = epoll.poll(1)
                for fileno, event in events:
                    if fileno == sock.fileno():
                        conn, addr = sock.accept()
                        conn.setblocking(0)
                        epoll.register(conn.fileno(), select.EPOLLIN)
                        connections[conn.fileno()] = conn
                    elif event & select.EPOLLIN:
                        data = connections[fileno].recv(
                            4096
                        )  # Don't care about this data either
                        epoll.modify(fileno, select.EPOLLOUT)
                    elif event & select.EPOLLOUT:
                        connections[fileno].send(
                            make_resp(correcthorsebatterystaple.generate()).encode()
                        )
                        epoll.modify(fileno, 0)
                        connections[fileno].shutdown(socket.SHUT_RDWR)
                    elif event & select.EPOLLHUP:
                        epoll.unregister(fileno)
                        connections[fileno].close()
                        del connections[fileno]
        except KeyboardInterrupt:
            print("Bye")
        finally:
            epoll.unregister(sock.fileno())
            epoll.close()


def ok_go(launch="single", host="127.0.0.1", port=80, gen=None):
    if launch == "single":
        single_server(host=host, port=port, correcthorsebatterystaple=gen)
    elif launch == "select":
        select_server(host=host, port=port, correcthorsebatterystaple=gen)
    elif launch == "epoll":
        epoll_server(host=host, port=port, correcthorsebatterystaple=gen)
    else:
        sys.exit("No launcher {} known!".format(launch))


def do_it():  # Shia LeBeouf!
    args = parser.parse_args()
    if args.version:
        print(__version__)
        sys.exit()
    root = args.root
    with open(os.path.join(root, "nouns.txt")) as f:
        nouns = f.read().splitlines()

    with open(os.path.join(root, "adjectives.txt")) as f:
        adjectives = f.read().splitlines()
    stapelerfahrer = CorrectHorseBatteryStaple(nouns=nouns, adjectives=adjectives)

    if args.one:
        print(stapelerfahrer.generate())
    else:
        ok_go(launch=args.launch, host=args.host, port=args.port, gen=stapelerfahrer)


if __name__ == "__main__":
    do_it()
