from ast import literal_eval
from functools import cmp_to_key

from utilities import get_puzzle

DATE = [2022, 13]


def compare(a, b) -> int:
    # validity_reason = str()
    int_validity = int()

    # Convert integers to lists
    left = a if isinstance(a, list) else [a]
    right = b if isinstance(b, list) else [b]

    for l_el, r_el in zip(left, right):
        # print(f"\tComparing: {l_el} to {r_el}")

        if isinstance(l_el, list) or isinstance(r_el, list):
            # If both values are lists, compare each value sequentially
            validity_check = compare(l_el, r_el)  # recursion
            int_validity = validity_check  # [0]
            # validity_reason = validity_check[1]
        else:
            # if both values are integers, do comparison
            int_validity = compare_ints(l_el, r_el)
            # validity_reason = "Integer comparison"

        if int_validity != 0:
            # if zero, the integers are the same, so continue checks
            break
    if int_validity == 0:
        return len(right) - len(left)  # , "List ran out"
    else:
        return int_validity  # , validity_reason


def compare_ints(a: int, b: int) -> int:
    # In correct order if right is higher than left
    # Not in correct order if left is higher than right
    if a == b:
        return 0
    return -1 if a > b else 1


def get_valid_packet_indices(pairs: list) -> list:
    valid_indices = list()
    for index, pair in enumerate(pairs):
        pair_list = pair.split("\n")
        # print(f"Raw Strings: {pair_list}")  # debug

        p1 = literal_eval(pair_list[0])
        p2 = literal_eval(pair_list[1])

        print(f"\nPair {index+1}: {p1}\t{p2}")  # debug

        is_valid = compare(p1, p2)
        print(f"{index+1}: {is_valid}")  # debug

        if is_valid >= 0:
            valid_indices.append(index + 1)
    return valid_indices


def main(debug: bool = False):

    puzzle = get_puzzle(year=DATE[0], day=DATE[1])
    input = puzzle.input_data

    # if debug is True:
    #     input = SAMPLE_DATA  # debug

    packet_pairs = input.split("\n\n")
    valid_packets = get_valid_packet_indices(packet_pairs)
    valid_packet_sum = sum(valid_packets)

    packets = [
        literal_eval(s) for s in input.replace("\n\n", "\n").split("\n")
    ]

    packets += [[[2]], [[6]]]
    sorted_packets = sorted(packets, key=cmp_to_key(compare), reverse=True)

    divider_product = (sorted_packets.index([[2]]) + 1) * (
        sorted_packets.index([[6]]) + 1
    )

    print(
        f"\nSum of valid packet indices: {valid_packet_sum}\n"
        f"Product of divider packet indices: {divider_product}\n"
    )
    # submit answers
    puzzle.answer_a = valid_packet_sum
    puzzle.answer_b = divider_product


if __name__ == "__main__":
    main()
