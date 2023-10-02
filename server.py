"""
Write code for your server here.

You may import library modules allowed by the specs, as well as your own other modules.
"""
from sys import argv
import sys
import socket
import typing

THISPORT = 1000;
# Load records from config_file
def load_records(config_file):
    records = dict()
    with open(config_file, 'r') as f:
        configdata=f.readlines()
    global THISPORT
    THISPORT = int(configdata[0])
    for line in configdata[1:]:
        hostname, port = line.strip().split(',')
        records[hostname] = int(port)
    return records


def handle_client(conn, records):
    data = conn.recv(THISPORT).decode().strip()
    if data.startswith("!"):
        # Command Handling
        parts = data[1:].split(' ')
        cmd = parts[0]
        if cmd == "ADD" and len(parts) == 3:
            hostname, port = parts[1], parts[2]
            if hostname not in records and 0 <= int(port) <= 65535:
                records[hostname] = int(port)
            elif hostname in records:
                records[hostname] = int(port)
        elif cmd == "DEL" and len(parts) == 2:
            hostname = parts[1]
            if hostname in records:
                del records[hostname]
        elif cmd == "EXIT":
            sys.exit(0)
        else:
            #sys.stdout.write("INVALID\n")
            pass
    elif data in records:
        conn.sendall((str(records[data])+"\n").encode())
        sys.stdout.write(f"resolve {data} to {records[data]}\n")
    else:
        conn.sendall(str("NXDOMAIN\n").encode())
        sys.stdout.write(f"resolve {data} to NXDOMAIN\n")

def main(args: list[str]) -> None:

    if len(args) != 1:
        sys.stdout.write("INVALID ARGUMENTS\n")
        sys.exit()

    config_file = args[0]
    records = load_records(config_file)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', THISPORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            with conn:
                handle_client(conn, records)


if __name__ == "__main__":
    main(argv[1:])
