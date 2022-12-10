from aocd.models import Puzzle

DATE = [2022, 9]

# get puzzle input
puzzle = Puzzle(year=DATE[0], day=DATE[1])
print(f"\nAdvent of Code {DATE[0]} Day {DATE[1]}: {puzzle.title}\n")
input = puzzle.input_data
#

# submit answers
# puzzle.answer_a = 0
# puzzle.answer_b = 0
