from aocd.models import Puzzle

DATE = [2022, 10]
TARGET_CYCLES = [20, 60, 100, 140, 180, 220]
ROW_LENGTH = 40


def sum_list_entries(src_list, entry_list) -> int:
    required_entries = [src_list[i - 1] for i in entry_list]
    print(f"\nRequested cycle strengths: {required_entries}")
    return sum(required_entries)


def process_cmd(cmd: str, prev_cycle_x: int) -> list[int]:
    updated_x = [prev_cycle_x]

    if cmd[0] == "a":
        addition = int(cmd.replace("addx ", ""))
        updated_x.append(prev_cycle_x + addition)
    return updated_x


def draw_pixel(row_str, pixel, x_val):
    sprite_location = [x_val - 1, x_val, x_val + 1]
    if pixel in sprite_location:
        row_str = f"{row_str[:pixel]}#{row_str[pixel+1:]}"
    return row_str


# get puzzle input
puzzle = Puzzle(year=DATE[0], day=DATE[1])
print(f"\nAdvent of Code {DATE[0]} Day {DATE[1]}: {puzzle.title}\n")
input = puzzle.input_data.split("\n")
#

x_val = 1
x_register = [x_val]
for line in input:
    x_register += process_cmd(line, x_val)
    x_val = x_register[-1]

cycle_strengths = list()
for index, x_val in enumerate(x_register):
    cycle = index + 1
    cycle_strength = cycle * x_val
    cycle_strengths.append(cycle_strength)
    print(f"{cycle} {x_val} {cycle_strength}")


# Find the signal strength during the 20th, 60th, 100th, 140th, 180th,
# and 220th cycles. What is the sum of these six signal strengths?
part_a_sum = sum_list_entries(cycle_strengths, TARGET_CYCLES)

print(f"Sum of signal strengths: {part_a_sum}\n")

# submit answers
puzzle.answer_a = part_a_sum

# part B can't be submitted automatically!
row_str = "." * 40
for index, x_val in enumerate(x_register):
    pixel = index % ROW_LENGTH
    if (pixel == 0) and (index != 0):
        # improve resolution for legibility!
        row_str = row_str.replace(".", "  ")
        row_str = row_str.replace("#", "##")
        print(row_str)
        row_str = "." * 40

    row_str = draw_pixel(row_str=row_str, pixel=pixel, x_val=x_val)

print("\n")
