"""
Write code for your recursor here.

You may import library modules allowed by the specs, as well as your own other modules.
"""
from sys import argv

import sys
import socket
import time

def is_valid_component(s):
    # Check if string s is non-empty and only contains alphanumeric or hyphen characters
    return s and all(c.isalnum() or c == '-' for c in s)


def verify_hostname(hostname):
    # Split the hostname by dots
    parts = hostname.split('.')

    # Ensure there are at least 3 components (A, B, C)
    if len(parts) < 3:
        return False

    # Validate A and B
    if not is_valid_component(parts[0]) or not is_valid_component(parts[1]):
        return False

    # Validate C
    # C should not start or end with a dot, so we ensured it by checking len(parts) >= 3 earlier
    for component in parts[2:]:
        # Make sure each component of C separated by a dot is valid
        if not is_valid_component(component):
            return False

    return True

def query_dns_server(server_port, query):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("localhost", server_port))
        s.sendall(query.encode())
        data = s.recv(1024)
    return data.decode()

def main(args: list[str]) -> None:
    # Check command-line arguments
    if len(sys.argv) != 3:
        print("INVALID ARGUMENTS\n")
        sys.exit(1)

    root_port = int(sys.argv[1])
    timeout = float(sys.argv[2])

    while True:
        try:
            hostname = input("Enter hostname to resolve: ")

            if not verify_hostname(hostname):
                sys.stdout.write("INVALID")
                continue

            parts = hostname.split('.')
            if len(parts) < 2:
                sys.stdout.write("INVALID")
                continue

            start_time = time.time()

            # Step 1
            tld_port = int(query_dns_server(root_port, parts[-1] + "\n"))

            # Step 2 and 3
            sld_port = int(query_dns_server(tld_port, ".".join(parts[-2:]) + "\n"))

            # Step 4 and 5
            final_port = int(query_dns_server(sld_port, hostname + "\n"))

            elapsed_time = time.time() - start_time
            if elapsed_time > timeout:
                sys.stdout.write("NXDOMAIN")
                continue

            sys.stdout.write(final_port, "\n")

        except EOFError:  # Handle Ctrl-D
            break
        except Exception as e:
            sys.stdout.write("Error:", e)
            continue


if __name__ == "__main__":
    main(argv[1:])
