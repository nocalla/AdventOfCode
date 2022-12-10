from collections import defaultdict

file = r"05_supply_stacks\input.txt"


def cull_strings(source: str, chars: list) -> str:
    for char in chars:
        source = source.replace(char, "")
    return source


def remove_list_entries(s_list: list, char: str) -> list:
    return [i for i in s_list if i != char]


def parse_command(cmd: str) -> list[int]:
    # move 3 from 8 to 9
    cmd_list = [0]
    if cmd[0] == "m":
        cmd_list = list()
        cmd = cull_strings(source=cmd, chars=["move ", "from ", "to ", "\n"])
        cmd_list = cmd.split(" ")
        cmd_list = list(map(int, cmd_list))
    return cmd_list


def update_stacks(count: int, source: list, dest: list):
    print(f"Count: {count}\nSource: {source}\nDest: {dest}")
    moved_elements = source[0:count]
    # moved_elements = list(reversed(moved_elements)) # uncomment for Part #1
    source = source[count:]
    dest = moved_elements + dest

    print(f"Amended Source: {source}\nAmended Dest: {dest}\n")

    return source, dest


with open(file, "r") as f:
    stacks = defaultdict(list)
    moving = False
    for line in f:
        if line[0] == "[":
            line = line.replace("    ", " [*]")
            line = cull_strings(source=line, chars=["[", "]", "\n"])
            row = line.split(" ")
            print(line)

            for index, item in enumerate(row):
                index += 1
                stacks[index].append(item)
        elif moving is False:
            moving = True
            print("\n")
            for col in stacks:
                stacks[col] = remove_list_entries(s_list=stacks[col], char="*")
                print(f"{col}: {stacks[col]}")
        else:
            command = parse_command(line)
            if command != [0]:
                new_source, new_dest = update_stacks(
                    count=command[0],
                    source=stacks[command[1]],
                    dest=stacks[command[2]],
                )
                stacks[command[1]] = new_source
                stacks[command[2]] = new_dest


stack_tops = str()
print("Final arrangement: ")
for col in stacks:
    print(f"{col}: {stacks[col]}")
    stack_tops = stack_tops + stacks[col][0]
print(f"Top of each stack: {stack_tops}")
