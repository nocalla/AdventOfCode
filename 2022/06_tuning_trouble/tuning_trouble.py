file = r"06_tuning_trouble\input.txt"
MARKER_LENGTH = 14  # set to 4 for part 1 and 14 for part 2


def get_marker_index(stream: str, marker_length: int) -> int:
    index = int()
    for index, char in enumerate(stream):
        test_marker = stream[index : index + marker_length]
        if all_unique_chars(test_marker):
            print(f"\nMarker: {test_marker}")
            break
    return index + marker_length


def all_unique_chars(input_str: str) -> bool:
    # sets do not allow duplicate values
    all_unique = False
    test_set = set(i for i in input_str)
    if len(input_str) == len(test_set):
        all_unique = True
    print(f"Set (unordered):{test_set}. All Unique: {all_unique}")
    return all_unique


with open(file, "r") as f:
    for line in f:
        index = get_marker_index(line, MARKER_LENGTH)
        print(f"Marker index: {index}\n")
