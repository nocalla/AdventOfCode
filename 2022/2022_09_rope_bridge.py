from ..utilities import get_puzzle

DATE = [2022, 9]  # year, day


def direction_mapping(dir_str: str) -> list[int]:
    dir_map = {"U": [0, 1], "D": [0, -1], "L": [-1, 0], "R": [1, 0]}
    return dir_map[dir_str]


def move_cmd(
    start_pos: list[int], dir: list[int], steps: int
) -> list[list[int]]:

    positions = [start_pos]
    for i in range(steps):
        pos = coord_add(positions[-1], dir)
        positions.append(pos)

    return positions[1:]


def coord_add(pos1: list[int], pos2: list[int]) -> list[int]:
    return [pos1[0] + pos2[0], pos1[1] + pos2[1]]


def get_distance(pos1: list[int], pos2: list[int]) -> int:
    x1 = pos1[0]
    y1 = pos1[1]
    x2 = pos2[0]
    y2 = pos2[1]

    return int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)


def get_dir(pos1: list[int], pos2: list[int]) -> list[int]:
    x1 = pos1[0]
    y1 = pos1[1]
    x2 = pos2[0]
    y2 = pos2[1]

    direction = [(x1 - x2), (y1 - y2)]

    return [normalise_int(direction[0]), normalise_int(direction[1])]


def normalise_int(i: int) -> int:
    if i == 0:
        return i
    return int(i / abs(i))


def get_follow_positions(h_positions):
    t_positions = [[0, 0]]
    t_pos = t_positions[-1]
    for h_pos in h_positions:
        dir = []
        dist = get_distance(pos1=h_pos, pos2=t_pos)
        if dist > 1:
            dir = get_dir(pos1=h_pos, pos2=t_pos)
            t_pos = move_cmd(start_pos=t_pos, dir=dir, steps=1)[-1]
            t_positions.append(t_pos)
        # print(f"{t_pos}\t->\t\t{h_pos}\t\tdistance: {dist}\tdirection:{dir}")
    return t_positions


def count_unique_entries(test_list: list[list[int]]) -> int:
    unique_entries = list()
    for entry in test_list:
        if entry not in unique_entries:
            unique_entries.append(entry)

    return len(unique_entries)


def get_follower_positions(
    lead_positions: list[list[int]], iterations: int
) -> list:
    follower_positions = list()

    previous_positions = lead_positions
    for i in range(iterations):
        previous_positions = get_follow_positions(previous_positions)
        follower_positions.append(previous_positions)

    return follower_positions


# get puzzle input
puzzle = get_puzzle(year=DATE[0], day=DATE[1])
input = puzzle.input_data
input_list = input.split("\n")
#

h_positions = [[0, 0]]

for line in input_list:

    cmd = line.split(" ")
    dir = direction_mapping(cmd[0])
    new_positions = move_cmd(
        start_pos=h_positions[-1], dir=dir, steps=int(cmd[1])
    )
    h_positions += new_positions

    # print(f"{line}: {new_positions}")

all_follower_positions = get_follower_positions(h_positions, 9)

first_follower_positions = all_follower_positions[0]
last_follower_positions = all_follower_positions[-1]

first_follower_pos_count = count_unique_entries(first_follower_positions)
last_follower_pos_count = count_unique_entries(last_follower_positions)

print(
    "\nUnique positions occupied by tail\n"
    f" {first_follower_pos_count}\nPart B: {last_follower_pos_count}"
)
puzzle.answer_a = first_follower_pos_count
puzzle.answer_b = last_follower_pos_count
