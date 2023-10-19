from sys import argv
from recursor import is_valid_domain
from pathlib import Path


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
            for line in master_data[1:]:
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
                parts = line.split(",")[0].split(".")
                for part in parts:
                    if not all(c.isalnum() or c == '-' for c in part):
                        print("invalid single")
                        exit(1)

    master_data = master_data[1:]

    def search_for_eq(match, port_key, og_key):
        for file in matching_files:
            with open(file, "r") as f:
                temp = f.readlines()

                if temp[0] == port_key or port_key == -1:
                    temp = temp[1:]
                    for line in temp:
                        parts = line.split(",")
                        if parts[0] == match and parts[1].strip() == og_key.strip() and port_key != -1:
                            return True
                        if (port_key == -1):
                            if (len(parts[0].split(".")) == 1):
                                if search_for_eq(match, parts[1], og_key):
                                    return True
                            else:
                                pass
                        else:
                            if search_for_eq(match, parts[1], og_key):
                                return True
        return False

    # print(key)

    result = True
    for line in master_data:
        parts = line.split(",")
        full_domain = parts[0]
        port = parts[1]
        try:
            result = result and search_for_eq(full_domain, -1, port)
        except OSError:
            print("neq")
            exit()

    if result:
        print("eq")
        exit()
    else:
        print("neq")
        exit()

    pass


if __name__ == "__main__":
    main(argv[1:])
