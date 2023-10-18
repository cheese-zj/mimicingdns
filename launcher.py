"""
Write code for your launcher here.

You may import library modules allowed by the specs, as well as your own other modules.
"""
from sys import argv
from recursor import is_valid_domain
from pathlib import Path

def main(args: list[str]) -> None:
    if len(args) != 2:
        print("INVALID ARGUMENTS")
        exit()
    master_file = str(args[0])
    dir_of_single_files = Path(str(args[1]))
    if not dir_of_single_files.is_dir():
        print("NON-WRITABLE SINGLE DIR")
        exit(1)
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
        print("INVALID MASTER")
        exit(1)
    pass


if __name__ == "__main__":
    main(argv[1:])
