file = r"2022_03_input.txt"


def check_line(s: str) -> int:
    item_count = len(s) - 1
    items_per_comp = int(item_count / 2)
    comp_1 = s[:items_per_comp]
    comp_2 = s[items_per_comp:]

    error_item = check_overlap(comp_1, comp_2)
    error_priority = get_priority(error_item)

    print(
        f"Items: {s}Count: {item_count}\nItems per Compartment:"
        f" {items_per_comp}\nCompartment 1: {comp_1}\nCompartment 2:"
        f" {comp_2}Error Item: {error_item}\nError Priority:"
        f" {error_priority}\n"
    )
    return error_priority


def get_priority(s) -> int:
    priority_string = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return priority_string.find(s) + 1


def check_overlap(s1: str, s2: str) -> str:
    e = str()
    for char in s1:
        if char in s2:
            e += char
    return e


def create_groups(file: str) -> list:
    bags = list()
    groups = list()

    with open(file, "r") as f:
        for line in f:
            bags.append(line[:-1])
    groups = [bags[x : x + 3] for x in range(0, len(bags), 3)]

    return groups


def get_common_item(group: list[str]) -> str:
    common_items = group[0]  # start with full first bag
    for bag in group[1:]:
        common_items = check_overlap(common_items, bag)
        print(common_items)
    return common_items[0]


with open(file, "r") as f:
    total_error_priorities = int()
    for s in f:
        total_error_priorities += check_line(s)


groups = create_groups(file)
total_badge_priorities = int()
for group in groups:
    common_item = get_common_item(group)
    item_priority = get_priority(common_item)
    total_badge_priorities += item_priority
    print(
        f"Group: {group}\nCommon Item: {common_item}\n"
        f"Item Priority: {item_priority}"
    )

print(
    f"Total Error Priority Score: {total_error_priorities}\n"
    f"Total Badge Priority Score: {total_badge_priorities}"
)
