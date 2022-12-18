from utilities import get_puzzle

DATE = [2022, 12]


def main():
    puzzle = get_puzzle(year=DATE[0], day=DATE[1])
    input = puzzle.input_data

    print(input)
    # submit answers
    # puzzle.answer_a = 0
    # puzzle.answer_b = 0


if __name__ == "__main__":
    main()
