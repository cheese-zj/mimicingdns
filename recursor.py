from sys import argv
import sys
import socket
import time


def is_valid_domain(domain):
    return all(s.isalnum() for s in domain.split("."))


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
            print("tld_info: "+tld_info)
            tld_port = int(tld_info)
        except ConnectionRefusedError:
            sys.stdout.write("FAILED TO CONNECT TO ROOT\n")
            sys.exit()

        domain_parts = domain.split('.')
        message = '.'.join(domain_parts[-2:]) + '\n'

        # Try to connect to the TLD server
        try:
            auth_info = query_server(tld_port, message, timeout)
            print("auth_info: "+auth_info)
            auth_port = int(auth_info)
        except ConnectionRefusedError:
            sys.stdout.write("FAILED TO CONNECT TO TLD\n")

        try:
            final_info = query_server(auth_port, domain + '\n', timeout)
            print("final_port: " + final_info)
            final_port = int(final_info)
            return str(final_port) + '\n'
        except ConnectionRefusedError:
            sys.stdout.write("FAILED TO CONNECT TO AUTH\n")

    except socket.timeout:
        return "NXDOMAIN\n"
    except ValueError:
        sys.stdout.write("INVALID\n")


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
            domain = input().strip()
            print("user_input: " + domain)
            if is_valid_domain(domain):
                sys.stdout.write(resolve_domain(root_port, domain, timeout))
            else:
                sys.stdout.write("INVALID\n")
    except EOFError:
        pass


if __name__ == "__main__":
    main(argv[1:])
