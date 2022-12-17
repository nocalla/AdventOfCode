from ..utilities import get_puzzle

DATE = [2022, 7]

PATH_SEPARATOR = "|"


def change_dir(cmd: str, path: str) -> str:
    print(cmd)
    cmd = cmd[5:].replace("..", "")

    if cmd == "":
        path = PATH_SEPARATOR.join(path.split(PATH_SEPARATOR)[:-1])
    else:
        path = f"{path}|{cmd}"
    return path


def get_filesize(details: str) -> int:
    filesize = int(details.split(" ")[0])
    return filesize


def get_parent_dir_paths(path: str) -> list[str]:
    parent_dirs = list()
    parents = current_dir.split(PATH_SEPARATOR)[1:-1]
    for index, dir in enumerate(parents):
        parent_path = PATH_SEPARATOR.join(
            path.split(PATH_SEPARATOR)[: -index - 1]
        )
        parent_dirs.append(parent_path)
    return parent_dirs


def get_final_sizes(sizes: list[int], limit: int) -> int:
    final_size = int()

    final_size = sum([i for i in sizes if i <= limit])
    print(f"\nFinal size: {final_size}\n")
    return final_size


def get_deleted_size(
    total_space: int, used_space: int, needed_space: int, sizes: list[int]
) -> int:
    dir_size = int()

    unused_space = total_space - used_space
    deletion_requirement = needed_space - unused_space
    sizes.sort()
    suitable_dirs = [i for i in sizes if i >= deletion_requirement]
    dir_size = suitable_dirs[0]
    print(f"Size of deleted directory: {dir_size}")
    return dir_size


puzzle = get_puzzle(year=DATE[0], day=DATE[1])
input = puzzle.input_data
input_list = input.split("\n")

dir_tree = {"|/": {"size": 0, "sub_directories": []}}
current_dir = ""
parent_dirs = list()

for line in input_list:
    # line = line.replace("\n", "")
    if line[0:4] == "$ cd":
        current_dir = change_dir(cmd=line, path=current_dir)
        parent_dirs = get_parent_dir_paths(current_dir)

        # print(f"CWD: {current_dir}, {parent_dirs}")

        if current_dir not in dir_tree:
            dir_tree[current_dir] = {"size": 0, "sub_directories": []}

    elif line[0:3] == "dir":
        dir_tree[current_dir]["sub_directories"].append(
            current_dir + PATH_SEPARATOR + line[4:]
        )
    elif line[0:4] != "$ ls":
        filesize = get_filesize(line)
        dir_tree[current_dir]["size"] += filesize

        for dir in parent_dirs:
            dir_tree[dir]["size"] += filesize

dir_sizes = list()
for key in dir_tree:
    # sum sub_directory size
    dir_size = dir_tree[key]["size"]
    dir_sizes.append(dir_size)

    print(f"Directory: {key}. Size: {dir_size}")

final_size = get_final_sizes(sizes=dir_sizes, limit=100000)
deleted_dir_size = get_deleted_size(
    total_space=70000000,
    used_space=dir_tree[PATH_SEPARATOR + "/"]["size"],
    needed_space=30000000,
    sizes=dir_sizes,
)
