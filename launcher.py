"""
Write code for your launcher here.

You may import library modules allowed by the specs, as well as your own other modules.
"""
from sys import argv
import sys
from recursor import is_valid_domain

def main(args: list[str]) -> None:
    if len(args) != 2:
        sys.stdout.write("INVALID ARGUMENTS\n")
        sys.exit()
    master_file = str(args[1])
    try:
        with open(master_file, "r") as f:
            master_data = f.readlines()
            master_port = int(master_data[0])
            if not 1024 <= master_port <= 65535:
                raise Exception
            for domain in master_data[1:]:
                if not is_valid_domain(domain):
                    raise Exception

    except (Exception, ValueError):
        sys.stdout.write("INVALID MASTER")
        sys.exit(1)

    dir_of_single_files = str(args[2])
    pass


if __name__ == "__main__":
    main(argv[1:])
