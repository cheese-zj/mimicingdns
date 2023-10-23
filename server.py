from sys import argv
import socket

THIS_PORT = 0
SAVED_INPUT = ""


# Load records from config_file
def load_records(config_file):
    records = dict()
    try:
        with open(config_file, 'r') as f:
            config_data = f.readlines()
            global THIS_PORT
            THIS_PORT = int(config_data[0])
            for line in config_data[1:]:
                hostname, port = line.strip().split(',')
                if all(s.isalnum() for s in hostname.split(".")):
                    records[hostname] = int(port)
                else:
                    raise Exception
    except (FileNotFoundError, TypeError, Exception, PermissionError):
        print("INVALID CONFIGURATION")
        exit(1)
    return records


def msg_buffer(conn):
    global SAVED_INPUT
    data = SAVED_INPUT + conn.recv(THIS_PORT).decode()
    messages = data.split("\n")

    # Last item could be a part of an incomplete message, popping it to the saved slot
    SAVED_INPUT = messages.pop()

    # Return list of complete messages
    return messages


def handle_client(conn, records):
    messages = msg_buffer(conn)
    for data in messages:
        if not data:  # Empty line, skip
            continue
        if data.startswith("!"):  # Command Handling
            parts = data[1:].split(' ')
            cmd = parts[0]
            if cmd == "ADD" and len(parts) == 3:
                hostname, port = parts[1], parts[2]
                if hostname not in records and 1024 <= int(port) <= 65535 \
                        and all(s.isalnum() for s in hostname.split(".")):
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
                conn.sendall("INVALID\n".encode())
        elif data in records:
            conn.sendall((str(records[data]) + "\n").encode())
            print(f"resolve {data} to {records[data]}")
        else:
            conn.sendall("NXDOMAIN\n".encode())
            print(f"resolve {data} to NXDOMAIN")
    conn.close()


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
        s.bind(("", THIS_PORT))
        s.listen()
    except (PermissionError, socket.timeout, OSError):
        print("INVALID CONFIGURATION")
        exit(1)

    while True:
        conn, addr = s.accept()
        handle_client(conn, records)


if __name__ == "__main__":
    main(argv[1:])
