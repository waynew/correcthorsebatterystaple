import os
import random
import socket
import os.path

root = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(root, "nouns.txt")) as f:
    nouns = f.read().splitlines()

with open(os.path.join(root, "adjectives.txt")) as f:
    adjectives = f.read().splitlines()


def generate_staple():
    return "{} {} {} {}".format(
        random.choice(adjectives),
        random.choice(nouns),
        random.choice(nouns),
        random.choice(nouns),
    )


def make_resp(data):
    return f"""\
HTTP/1.1 200 OK
Server: correcthorsebatterystaple/1.0.0
Content-Type: text/plain
Content-Length: {len(data)}

{data}"""


def do_it(host="127.0.0.1", port=80):  # Shia LeBeouf!
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
                client.send(make_resp(generate_staple()).encode())
                client.close()
        except KeyboardInterrupt:
            print("Bye")


if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 8000))
    do_it(host=host, port=port)
