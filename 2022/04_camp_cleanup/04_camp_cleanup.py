import re

file = r"04_camp_cleanup\input.txt"


def check_fully_contained(
    start1: int, end1: int, start2: int, end2: int
) -> bool:
    is_contained = bool()

    if (start1 >= start2) and (end1 <= end2):
        is_contained = True
    if (start2 >= start1) and (end2 <= end1):
        is_contained = True

    return is_contained


def check_overlapping(start1: int, end1: int, start2: int, end2: int) -> bool:
    is_overlapping = bool()

    if (start1 >= start2) and (start1 <= end2):
        is_overlapping = True
    if (start2 >= start1) and (start2 <= end1):
        is_overlapping = True

    return is_overlapping


with open(file, "r") as f:
    pairs = list()
    full_contained_ranges = int()
    overlapping_ranges = int()
    for line in f:
        # split line into list of start and end points
        pair = re.split(pattern=r",|-|\n", string=line)[:-1]

        range_contained = check_fully_contained(
            int(pair[0]), int(pair[1]), int(pair[2]), int(pair[3])
        )
        range_overlaps = check_overlapping(
            int(pair[0]), int(pair[1]), int(pair[2]), int(pair[3])
        )

        print(
            f"Pair: {pair[0]}-{pair[1]} & {pair[2]}-{pair[3]}\n"
            f"Fully Contained: {range_contained}\n"
            f"Overlap: {range_overlaps}\n"
        )

        if range_contained is True:
            full_contained_ranges += 1
        if range_overlaps is True:
            overlapping_ranges += 1


print(
    f"Total fully-contained ranges: {full_contained_ranges}\n"
    f"Total ranges with overlaps: {overlapping_ranges}"
)
