from sys import argv
import socket
import time


def is_valid_domain(domain):
    if not domain:
        return False

    # Split by dots
    parts = domain.split('.')

    # Ensure there are at least 3 parts (AUTH, TLD, ROOT)
    if len(parts) < 3:
        return False

    # Validate ROOT and TLD
    if not all(all(c.isalnum() or c == '-' for c in part) for part in parts[-2:]):
        return False
    # Validate AUTH
    auth = ".".join(parts[:-2])
    if auth.startswith('.') or auth.endswith('.'):
        return False
    if not all(c.isalnum() or c in ['-', '.'] for c in auth):
        return False
    return True

# Function to query a server on a specific port with a given message
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

        # Query the root server for the TLD port
        try:
            tld_info = query_server(port, message, timeout)
            tld_port = int(tld_info)
        except ConnectionRefusedError:
            print("FAILED TO CONNECT TO ROOT")
            exit(1)

        domain_parts = domain.split('.')
        message = '.'.join(domain_parts[-2:]) + '\n'

        # Query the TLD server for the AUTH's port
        try:
            auth_info = query_server(tld_port, message, timeout)
            auth_port = int(auth_info)
        except ConnectionRefusedError:
            print("FAILED TO CONNECT TO TLD")
            exit(1)

        # Query the AUTH server for the final port
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

    # Parse arguments for root server port and timeout
    try:
        root_port = int(args[0])
        if not (0 <= root_port <= 65535):
            raise ValueError
        timeout = float(args[1])
    except ValueError:
        print("INVALID ARGUMENTS")
        exit()

    # Keep reading domain names and resolving them until EOF
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
