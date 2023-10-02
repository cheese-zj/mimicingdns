"""
Write code for your recursor here.

You may import library modules allowed by the specs, as well as your own other modules.
"""
from sys import argv

import sys
import socket
import time


def is_valid_domain(domain):
    # A basic domain validation for this example; can be extended
    if any(len(part) == 0 for part in domain.split('.')):
        return False
    return True


def query_server(port, message, timeout):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        s.connect(('127.0.0.1', port))
        s.sendall(message.encode())
        data = s.recv(1024).decode()
    return data


def resolve_domain(root_port, domain, timeout):
    start_time = time.time()
    try:
        # Step 1
        port = root_port
        message = domain.split('.')[-1] + '\n'
        tld_port = int(query_server(port, message, timeout))

        # Step 2 and 3
        domain_parts = domain.split('.')
        message = '.'.join(domain_parts[-2:]) + '\n'
        auth_port = int(query_server(tld_port, message, timeout))

        # Step 4, 5 and 6
        final_port = int(query_server(auth_port, domain + '\n', timeout))
        return str(final_port) + '\n'

    except (socket.timeout, ValueError):
        elapsed_time = time.time() - start_time
        if elapsed_time > timeout:
            return "NXDOMAIN"
        else:
            return "ERROR"


def main(args: list[str]) -> None:
    if len(args) != 2:
        sys.stdout.write("INVALID ARGUMENTS\n")
        sys.exit()

    try:
        root_port = int(args[0])
        if not (0 <= root_port <= 65535):
            raise ValueError
        timeout = float(args[1])
    except ValueError:
        sys.stdout.write("INVALID ARGUMENTS\n")
        sys.exit()

    try:
        while True:
            domain = input("Input a domain").strip()
            if is_valid_domain(domain):
                sys.stdout.write(resolve_domain(root_port, domain, timeout))
            else:
                sys.stdout.write("INVALID\n")
    except EOFError:
        pass
    except ConnectionRefusedError:
        sys.stdout.write("FAILED TO CONNECT TO ROOT\n")
        sys.exit()

if __name__ == "__main__":
    main(argv[1:])
