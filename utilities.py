from aocd.models import Puzzle


def get_puzzle(year: int, day: int) -> Puzzle:
    puzzle = Puzzle(year, day)
    print(f"\nAdvent of Code {day} Day {year}: {puzzle.title}\n")
    return puzzle


def add_xy_coord(v1, v2):
    return (v1[0] + v2[0], v1[1] + v2[1])
