import argparse
import os
import os.path
import random
import socket


parser = argparse.ArgumentParser()
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
    choices=("single", "select"),
    help="The type of server to run.",
    default="single",
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
        sock.listen(1)
        try:
            while True:
                print("Listening for connection...")
                client, addr = sock.accept()
                print(f"Connection from {addr[0]}:{addr[1]}")
                data = client.recv(4096)  # This should be enough for the HTML header
                client.send(make_resp(gen.generate()).encode())
                client.close()
        except KeyboardInterrupt:
            print("Bye")


def do_it(launch="single", host="127.0.0.1", port=80, gen=None):  # Shia LeBeouf!
    if launch == "single":
        single_server(host=host, port=port, correcthorsebatterystaple=gen)
    else:
        sys.exit("No launcher {} known!".format(launch))


if __name__ == "__main__":
    args = parser.parse_args()
    root = args.root
    with open(os.path.join(root, "nouns.txt")) as f:
        nouns = f.read().splitlines()

    with open(os.path.join(root, "adjectives.txt")) as f:
        adjectives = f.read().splitlines()
    stapelerfahrer = CorrectHorseBatteryStaple(nouns=nouns, adjectives=adjectives)

    do_it(launch=args.launch, host=args.host, port=args.port, gen=stapelerfahrer)
