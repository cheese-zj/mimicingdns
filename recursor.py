from sys import argv
import socket
import time


def is_valid_domain(domain):
    if not domain:
        return False

    # Split by dots
    parts = domain.split('.')

    # Ensure there are at least 3 parts (C, B, A)
    if len(parts) < 3:
        return False

    # Validate A and B
    if not all(all(c.isalnum() or c == '-' for c in part) for part in parts[-2:]):
        return False
    # Validate C
    C = ".".join(parts[:-2])
    if C.startswith('.') or C.endswith('.'):
        return False
    if not all(c.isalnum() or c in ['-', '.'] for c in C):
        return False
    return True


def query_server(port, message, timeout):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        s.connect(("", port))
        s.sendall(message.encode())
        data = s.recv(1024).decode()
    return data


def resolve_domain(root_port, domain, timeout):
    start_time = time.time()
    try:
        port = root_port
        message = domain.split('.')[-1] + '\n'

        # Try to connect to the root server
        try:
            tld_info = query_server(port, message, timeout)
            tld_port = int(tld_info)
        except ConnectionRefusedError:
            print("FAILED TO CONNECT TO ROOT")
            exit(1)

        domain_parts = domain.split('.')
        message = '.'.join(domain_parts[-2:]) + '\n'

        # Try to connect to the TLD server
        try:
            auth_info = query_server(tld_port, message, timeout)
            auth_port = int(auth_info)
        except ConnectionRefusedError:
            print("FAILED TO CONNECT TO TLD")
            exit(1)

        try:
            final_info = query_server(auth_port, domain + '\n', timeout)
            final_port = int(final_info)
            return str(final_port)
        except ConnectionRefusedError:
            print("FAILED TO CONNECT TO AUTH")
            exit(1)

    except (ValueError, socket.timeout):
        return "NXDOMAIN"


def main(args: list[str]) -> None:
    if len(args) != 2:
        print("INVALID ARGUMENTS")
        exit()

    try:
        root_port = int(args[0])
        if not (0 <= root_port <= 65535):
            raise ValueError
        timeout = float(args[1])
    except ValueError:
        print("INVALID ARGUMENTS")
        exit()

    try:
        while True:
            domain = input()
            if is_valid_domain(domain):
                print(resolve_domain(root_port, domain, timeout))
            else:
                print("INVALID")
    except EOFError:
        pass


if __name__ == "__main__":
    main(argv[1:])
