"""
Write code for your server here.

You may import library modules allowed by the specs, as well as your own other modules.
"""
from sys import argv
import socket

THISPORT = 1000
# Load records from config_file
def load_records(config_file):
    records = dict()
    try:
        with open(config_file, 'r') as f:
            configdata=f.readlines()
            global THISPORT
            THISPORT = int(configdata[0])
            for line in configdata[1:]:
                hostname, port = line.strip().split(',')
                if all(s.isalnum() for s in hostname.split(".")):
                    records[hostname] = int(port)
                else:
                    raise Exception
    except (FileNotFoundError, TypeError, Exception):
        print("INVALID CONFIGURATION")
        exit(1)
    return records


def handle_client(conn, records):
    data = conn.recv(THISPORT).decode().strip()
    if data.startswith("!"):
        # Command Handling
        parts = data[1:].split(' ')
        cmd = parts[0]
        if cmd == "ADD" and len(parts) == 3:
            hostname, port = parts[1], parts[2]
            if hostname not in records and 1024 <= int(port) <= 65535:
                records[hostname] = int(port)
            elif hostname in records:
                records[hostname] = int(port)
        elif cmd == "DEL" and len(parts) == 2:
            hostname = parts[1]
            if hostname in records:
                del records[hostname]
        elif cmd == "EXIT":
            exit(0)
        else:
            print("INVALID")
    elif data in records:
        conn.sendall((str(records[data])).encode()+"\n")
        print(f"resolve {data} to {records[data]}")
    else:
        conn.sendall("NXDOMAIN\n".encode())
        print(f"resolve {data} to NXDOMAIN")

def main(args: list[str]) -> None:

    if len(args) != 1:
        print("INVALID ARGUMENTS")
        exit()

    config_file = args[0]
    records = load_records(config_file)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # https://stackoverflow.com/questions/6380057/python-binding-socket-address-already-in-use

    try:
        s.bind(("", THISPORT))
        s.listen()
    except (PermissionError, socket.timeout):
        print("INVALID CONFIGURATION")
        exit(1)

    while True:
        conn, addr = s.accept()
        handle_client(conn, records)

if __name__ == "__main__":
    main(argv[1:])
