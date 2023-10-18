"""
Write code for your verifier here.

You may import library modules allowed by the specs, as well as your own other modules.
"""
from sys import argv

from recursor import is_valid_domain
from pathlib import Path


def part_check():


def main(args: list[str]) -> None:
    if len(args) != 2:
        print("invalid arguments")
        exit()
    master_file = str(args[0])
    dir_of_single_files = str(args[1])
    if Path(dir_of_single_files).is_dir() is False:
        print("singles io error")
        exit(1)
    try:
        with open(master_file, "r") as f:
            master_data = f.readlines()
            master_port = int(master_data[0])
            if not 1024 <= master_port <= 65535:
                raise Exception
            master_data = master_data[1:]
            for line in master_data:
                domain = line.split(",")[0]
                if not is_valid_domain(domain):
                    raise Exception
                port = int(line.split(",")[1])
                if not 1024 <= port <= 65535:
                    raise Exception

    except (Exception, ValueError):
        print("invalid master")
        exit(1)

    search_dir = Path(dir_of_single_files)
    matching_files = list(search_dir.glob("*.conf"))

    # Single file validation:
    for file in matching_files:
        with open(file, "r") as f:
            data = f.readlines()[1:]
            for line in data:
                parts = line.split(",")[0]
                if not all(c.isalnum() or c == '-' for c in part for part in parts):
                    print("invalid single")
                    exit(1)


    pass



if __name__ == "__main__":
    main(argv[1:])
