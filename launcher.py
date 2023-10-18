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
    dir_of_single_files = str(args[1])
    if Path(dir_of_single_files).is_dir() is False:
        print("NON-WRITABLE SINGLE DIR")
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
                #print(domain)
                if not is_valid_domain(domain):
                    raise Exception
                port = int(line.split(",")[1])
                #print(port)
                if not 1024 <= port <= 65535:
                    raise Exception

        roots = set()
        auth = dict()
        used_port = set()

        port_pointer = master_port

        def pointer_mover():
            pointer = port_pointer
            pointer += 1
            while pointer in used_port:
                pointer += 1
            used_port.add(pointer)
            return pointer

        for line in master_data:
            reflect = line.split(",")
            auth[reflect[0]]=int(reflect[1].strip())
            used_port.add(int(reflect[1].strip()))
            roots.add(reflect[0].split(".")[-1])  # add roots eg "com" into roots set
        with open(dir_of_single_files+"/root.conf", "w") as root_f:
            root_f.write(str(port_pointer)+"\n")
            port_pointer = pointer_mover()
            for root in roots:
                root_f.write(root+","+str(port_pointer)+"\n")
                port_pointer = pointer_mover()

        with open(dir_of_single_files + "/root.conf", "r") as root_f:
            data = root_f.readlines()[1:]
            for line in data:
                line = line.split(",")
                with open(dir_of_single_files + "/tld-" + line[0] + ".conf", "w") as tld_f:
                    tld_f.write(line[1].strip()+"\n")
                    for item in auth:
                        if item.split(".")[-1] == line[0]:
                            parts = item.split(".")
                            domain = f"{parts[-2]}.{parts[-1]}"
                            tld_f.write(f"{domain},{port_pointer}\n")
                            port_pointer = pointer_mover()

        search_dir = Path(dir_of_single_files)
        # Find all files that start with 'tld-'
        matching_files = list(search_dir.glob("tld-*"))
        for file in matching_files:
            with open(file, "r") as tld_f:
                data = tld_f.readlines()[1:]
                for line in data:
                    line = line.split(",")
                    f_dir = dir_of_single_files + "/auth-" + line[0].split(".")[0] + ".conf"
                    with open(f_dir, "w") as auth_f:
                        auth_f.write(line[1].strip()+"\n")
                        for item in auth:
                            if item.split(".")[-2]+"."+item.split(".")[-1] == line[0]:
                                auth_f.write(f"{item},{auth[item]}\n")




    except (Exception, ValueError):
        print("INVALID MASTER")
        exit(1)
    pass


if __name__ == "__main__":
    main(argv[1:])
