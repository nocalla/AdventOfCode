from ..utilities import get_puzzle

INPUT_FILE = r"08_treetop_tree_house\input.txt"
DATE = [2022, 8]


def check_visibility(
    col_index: int,
    height_str: str,
    row_index: int,
    row: str,
    rows: list[str],
    all_potential_blocks: list[list[int]],
) -> int:

    # border trees are always visible
    if border_check(row_index, col_index, len(row) - 1, len(rows) - 1) is True:
        return 1

    height = int(height_str)

    for potential_blocks in all_potential_blocks:
        visible = test_blockade(height=height, test_vals=potential_blocks)
        if visible is True:
            return 1
    return 0


def border_check(
    row_index: int, col_index: int, row_len: int, row_count: int
) -> bool:
    if (
        row_index == 0
        or row_index == row_count
        or col_index == 0
        or col_index == row_len
    ):
        return True
    return False


def get_potential_blocks(
    col_index: int, row_index: int, row: str, rows: list[str]
):
    return row_blocks(index=col_index, row=row) + col_blocks(
        col_index=col_index, row_index=row_index, rows=rows
    )


def test_blockade(height: int, test_vals: list[int]) -> bool:
    successful_blocks = [i for i in test_vals if i >= height]
    if len(successful_blocks) > 0:
        return False
    return True


def row_blocks(index: int, row: str) -> list[list[int]]:

    blocks = [*row]
    blocks = [int(s) for s in blocks]
    blocks_1 = blocks[:index]
    blocks_2 = blocks[index + 1 :]

    return [blocks_1, blocks_2]


def col_blocks(
    col_index: int, row_index: int, rows: list[str]
) -> list[list[int]]:

    col = list()

    for row in rows:
        col.append(int(row[col_index]))
    blocks_1 = col[:row_index]
    blocks_2 = col[row_index + 1 :]

    return [blocks_1, blocks_2]


def get_scenic_score(
    height_str: str, all_potential_blocks: list[list[int]]
) -> int:
    scenic_score = 1
    height = int(height_str)
    # left, right, up, down
    view_distances = {
        "left": list(reversed(all_potential_blocks[0])),
        "right": all_potential_blocks[1],
        "up": list(reversed(all_potential_blocks[2])),
        "down": all_potential_blocks[3],
    }

    for key in view_distances:
        view = view_distances[key]
        scenic_score *= get_view_distance(height, view)

    return scenic_score


def get_view_distance(height: int, view: list[int]) -> int:
    score = int()

    for val in view:
        score += 1
        if val >= height:
            return score
    return score


puzzle = get_puzzle(year=DATE[0], day=DATE[1])
input = puzzle.input_data
tree_rows = input.split("\n")[:-1]

visible_trees = int()
tree_rows = list()
tree_map = str()
scenic_scores = list()

for row_index, row in enumerate(tree_rows):
    tree_map += "\n"
    row_len = len(row)

    for index, height_str in enumerate(row):
        all_potential_blocks = get_potential_blocks(
            col_index=index, row_index=row_index, row=row, rows=tree_rows
        )
        visible = check_visibility(
            col_index=index,
            height_str=height_str,
            row_index=row_index,
            row=row,
            rows=tree_rows,
            all_potential_blocks=all_potential_blocks,
        )

        visible_trees += visible
        if visible == 0:
            tree_map += "_"
        else:
            tree_map += str(height_str)

        if (
            border_check(row_index, index, len(row) - 1, len(tree_rows) - 1)
            is False
        ):
            scenic_scores.append(
                get_scenic_score(
                    height_str=height_str,
                    all_potential_blocks=all_potential_blocks,
                )
            )

print(tree_map)
print(
    f"\nTotal visible trees: {visible_trees}\nMax. possible scenic score:"
    f" {max(scenic_scores)}\n"
)
