from collections import defaultdict
from typing import Tuple

from ..aoc_utilities.utilities import add_xy_coord, get_puzzle

DATE = [2022, 12]

xy_coord = Tuple[int, int]  # custom type hint for XY coordinate Tuple


class Vertex:
    def __init__(
        self,
        coord: xy_coord = (0, 0),
        char: str = "",
        height: int = 9999,
        connected_coords: list[xy_coord] = [],
    ) -> None:

        self.coord: xy_coord = coord
        self.char: str = char
        self.height: int = height
        self.connected: list[xy_coord] = connected_coords
        # self.visited: int = -1
        self.level_dict: dict = dict(defaultdict())

    def update_level(self, iteration: int, level: int) -> None:
        self.level_dict[iteration] = level

    def update_char(self, s: str) -> None:
        self.char = s

    def update_height(self, i: int) -> None:
        self.height = i

    # def update_visited(self, i: int) -> None:
    #     self.visited = i


def list2grid(lst: list[str]) -> Tuple[dict[xy_coord, Vertex], xy_coord]:
    """
    Turns a list of strings into a dict representing
    a grid of vertices of coordinate (X,Y).

    :param lst: A list of strings where each element
    of the list corresponds to a row of the XY grid
    :type lst: list
    :return: A Tuple where the first value is a dictionary
    of XY coordinates mapped to matching string character
    and the second value is the maximum XY coordinate in the grid
    :rtype: Tuple[dict, xy_coord]
    """
    grid = defaultdict(Vertex)
    max_x = len(lst[0])
    max_y = len(lst[0])
    max_coord = (max_x, max_y)

    for y, row in enumerate(lst):
        for x, char in enumerate(row):
            coord = (x, y)
            height = alpha_to_int(char)  # turn letters into integers
            connected_coords = get_connected_coords(coord, max_coord)
            grid[coord] = Vertex(
                coord=coord,
                char=char,
                height=height,
                connected_coords=connected_coords,
            )
    return grid, max_coord


def get_connected_coords(
    coord: xy_coord, max_coord: xy_coord
) -> list[xy_coord]:
    connected_coords = list()
    offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    for neighbour_offset in offsets:
        neighbour_coord = add_xy_coord(coord, neighbour_offset)
        if test_valid_coord(v1=neighbour_coord, v2=max_coord) is True:
            connected_coords.append(neighbour_coord)

    return connected_coords


def test_valid_coord(v1: xy_coord, v2: xy_coord):
    if v1[0] >= 0 and v1[1] >= 0 and v1[0] <= v2[0] and v1[1] <= v2[1]:
        return True
    return False


def is_traversable(h1: int, h2: int) -> bool:

    if h2 - h1 > 1:
        return False
    return True


def get_endpoints(grid) -> Tuple[xy_coord, xy_coord]:
    start_coord = (0, 0)
    end_coord = (0, 0)
    for key in grid.keys():
        updated_char = str()
        vert = grid[key]
        if vert.char == "S":
            start_coord = key
            updated_char = "a"
        elif vert.char == "E":
            end_coord = key
            updated_char = "z"
        if updated_char != "":
            vert.update_char(updated_char)
            vert.update_height(alpha_to_int(updated_char))

    return start_coord, end_coord


def alpha_to_int(char: str) -> int:
    return ord(char) - 97


def breadth_first_search(
    grid: dict[xy_coord, Vertex],
    start_coord: xy_coord,
    end_coord: xy_coord,
    iteration: int,
) -> Tuple[dict, bool, int]:

    queue = list()
    path_length = int()
    destination_reached = False
    queue.append(start_coord)
    grid[start_coord].update_level(iteration=iteration, level=0)

    while len(queue) > 0:
        current_coord = queue.pop(0)
        current = grid[current_coord]
        path_length = current.level_dict[iteration]
        if current_coord == end_coord:
            print(
                f"Iteration: {iteration} - Destination reached:"
                f" {current_coord} - Path Length: {path_length}"
            )
            destination_reached = True
            break
        for neighbour_coord in current.connected:
            neighbour = grid[neighbour_coord]
            # print(neighbour.level_dict[iteration])
            # debug_height_differential(current, neighbour) # debug

            if (
                iteration not in neighbour.level_dict.keys()
                and is_traversable(current.height, neighbour.height) is True
            ):

                queue.append(neighbour.coord)
                neighbour.update_level(
                    iteration=iteration, level=path_length + 1
                )
        # break  # debug

    return grid, destination_reached, path_length


def debug_height_differential(v1: Vertex, v2: Vertex) -> None:
    print(
        f"{v1.coord} ({v1.char} = {v1.height}) -> "
        f"{v2.coord} ({v2.char} = {v2.height})  "
        f" \t[{v2.height} - {v1.height} ="
        f" {v2.height-v1.height}]"
    )


def visualise_grid(input_list: list[str], grid: dict) -> None:
    for y in range(len(input_list)):
        row = input_list[y]
        for x in range(len(row)):
            if grid[(x, y)].visited is True:
                row = row[:x] + row[x].upper() + row[x + 1 :]
                # row = row[:x] + "_" + row[x + 1 :]
        print(f"{row}")


def get_all_points_at_height(
    grid: dict[xy_coord, Vertex], height: int
) -> list[xy_coord]:
    points = list()
    for key in grid.keys():
        if grid[key].height == height:
            points.append(key)
    return points


def main():
    puzzle = get_puzzle(year=DATE[0], day=DATE[1])
    input = puzzle.input_data
    input_list = input.split("\n")

    grid, max_coord = list2grid(input_list)
    start_coord, end_coord = get_endpoints(grid)
    # updated_grid, dest_reached, path_length = breadth_first_search(
    #     grid, start_coord, end_coord
    # ) # this works but it doesn't work in the loop for some reason

    # visualise_grid(input_list, updated_grid)  # debug
    path_lengths = list()
    path_length = int()
    initial_shortest_path = int()
    low_points = get_all_points_at_height(grid, 0)

    print(f"Calculating path from {len(low_points)} start points...")

    for iteration, point in enumerate(low_points):
        updated_grid, dest_reached, path_length = breadth_first_search(
            grid,
            point,
            end_coord,
            iteration=iteration,
        )
        if dest_reached is False:
            print(f"Destination not reached for iteration {iteration}!")
        else:
            if point == start_coord:
                initial_shortest_path = path_length
            path_lengths.append(path_length)
    shortest_path = min(path_lengths)

    print(
        f"\nPart A - Shortest Path Length: {initial_shortest_path}\n"
        f"Part B - Shortest Path Length of all low points: {shortest_path}\n"
    )
    # submit answer A
    puzzle.answer_a = initial_shortest_path
    # submit answer B
    puzzle.answer_b = shortest_path


if __name__ == "__main__":
    main()
