
from sys import argv

import sys
import socket
import time


def resolve_domain(domain, root_port, timeout):
    # Split the domain into parts
    parts = domain.split('.')
    tld = parts[-2] if len(parts) > 1 else None
    name = parts[-1]

    # Create a socket and connect to the root server
    try:
        s = socket.create_connection(('localhost', root_port), timeout)
    except (socket.timeout, ConnectionRefusedError):
        sys.stdout.write("FAILED TO CONNECT TO ROOT\n")
        sys.exit(1)
    except EOFError:
        pass

    # Start the timer
    start_time = time.time()

    # Send the TLD to the root server
    s.sendall(tld.encode() + b"\n")
    port = int(s.recv(1024).decode().strip())

    # Connect to the TLD server
    try:
        s = socket.create_connection(('localhost', port), timeout)
    except EOFError:
        pass
    except (socket.timeout, ConnectionRefusedError):
        sys.stdout.write("FAILED TO CONNECT TO TLD\n")
        sys.exit(1)


    # Send the name to the TLD server
    s.sendall(name.encode() + b"\n")
    port = int(s.recv(1024).decode().strip())

    # End the timer
    elapsed_time = time.time() - start_time

    # Check for timeout
    if elapsed_time > timeout:
        sys.stdout.write("NXDOMAIN\n")
        return

    # Print the final result
    print(f"{port}\n")


def main():
    # Check command-line arguments
    if len(sys.argv) != 3:
        sys.stdout.write("INVALID ARGUMENTS\n")
        sys.exit(1)

    root_port = int(sys.argv[1])
    timeout = float(sys.argv[2])  # Can be an integer or float

    # Infinite loop to continuously take user input
    while True:
        domain = input().strip()
        # if not domain:  # If the user pressed just Enter, continue
        #     continue
        # elif domain == '\x04':  # Ctrl+D
        #     break
        # else:
            # Validate the domain
        if not all(part.isalnum() for part in domain.split('.')):
            sys.stdout.write("INVALID\n")
        else:
            resolve_domain(domain, root_port, timeout)



if __name__ == "__main__":
    main()

