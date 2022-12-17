from ast import literal_eval

from ..utilities import get_puzzle

DATE = [2022, 11]
WORRY_REDUCTION = False  # set to True for Part A, False for Part B
ROUNDS = 10000  # set to 20 for Part A, 10000 for Part B


class Monkey:
    def __init__(
        self,
        index: int,
        items: list[int],
        operation: list[str],
        test: int,
        false_target: int,
        true_target: int,
    ) -> None:
        self.index = index
        self.items = items
        self.operation = operation
        self.test = test
        self.false_target = false_target
        self.true_target = true_target
        self.items_checked = int()

    def print_params(self):
        print(
            f"{self.index}, {self.items}, {self.operation}, {self.test},"
            f" {self.false_target}, {self.true_target}, {self.items_checked}"
        )

    def check_items(self) -> list[list[int]]:
        items_to_pass = list()
        for old_score in self.items:
            self.items_checked += 1
            score = apply_operation(old_score, self.operation)
            if WORRY_REDUCTION is True:
                score /= 3
            score = int(score)
            test_result = test_divisible(score, self.test)
            target = self.true_target
            if test_result is False:
                target = self.false_target
            items_to_pass.append([target, score])
        self.items = []
        return items_to_pass

    def accept_item(self, score: int):
        self.items.append(score)


def apply_operation(old: int, operation: list[str]):
    operator = operation[0]
    value_str = operation[1]
    if value_str == "old":
        value_str = str(old)
    value = int(value_str)
    new_score = old

    if operator == "+":
        new_score += value
    elif operator == "-":
        new_score -= value
    elif operator == "*":
        new_score *= value
    elif operator == "/":
        new_score /= value
    return int(new_score)


def test_divisible(val: int, divisor: int) -> bool:
    test_bool = False
    if val % divisor == 0:
        test_bool = True
    return test_bool


def process_input(input_str) -> list[list]:
    param_list = list()
    input_list = input_str.split("\n\n")

    for monkey in input_list:
        monkey = remove_substrings(monkey)
        raw_monkey_params = monkey.split("\n  ")

        monkey_items = raw_monkey_params[1].split(", ")

        params = [
            int(raw_monkey_params[0][:-1]),
            [literal_eval(i) for i in monkey_items],
            raw_monkey_params[2].split(" "),
            int(raw_monkey_params[3]),
            int(raw_monkey_params[4]),
            int(raw_monkey_params[5]),
        ]

        param_list.append(params)

    return param_list


def remove_substrings(input_str: str) -> str:
    to_remove = [
        "Monkey ",
        "Starting items: ",
        "Operation: new = old ",
        "Test: divisible by ",
        "  If true: throw to monkey ",
        "  If false: throw to monkey ",
    ]
    cleaned_str = input_str
    for substring in to_remove:
        cleaned_str = cleaned_str.replace(substring, "")
    return cleaned_str


# get puzzle input
puzzle = get_puzzle(year=DATE[0], day=DATE[1])
input = puzzle.input_data
#

parameter_list = process_input(input)

monkey_list = list()
for monkey_params in parameter_list:
    monkey_list.append(
        Monkey(
            index=monkey_params[0],
            items=monkey_params[1],
            operation=monkey_params[2],
            test=monkey_params[3],
            true_target=monkey_params[4],
            false_target=monkey_params[5],
        )
    )

test_cycle_length = 1  # for fixing huge numbers
for monkey_obj in monkey_list:
    monkey_obj.print_params()
    test_cycle_length *= monkey_obj.test  # for fixing huge numbers
print("\n")

for i in range(ROUNDS):
    for monkey_obj in monkey_list:
        print(f"Round {i+1} - processing Monkey {monkey_obj.index}...")
        items_to_pass = monkey_obj.check_items()
        for monkey, item in items_to_pass:
            item = item % test_cycle_length  # for fixing huge numbers
            monkey_list[monkey].accept_item(item)

print(f"\nAfter {ROUNDS} rounds:")
monkey_counts = list()
for monkey_obj in monkey_list:
    monkey_obj.print_params()
    monkey_counts.append(monkey_obj.items_checked)

monkey_counts.sort(reverse=True)
monkey_business = monkey_counts[0] * monkey_counts[1]
print(
    f"Monkey business = {monkey_counts[0]} * {monkey_counts[1]} ="
    f" {monkey_business}"
)

# submit answers
# puzzle.answer_a = monkey_business
puzzle.answer_b = monkey_business
