import enum
from pathlib import Path
from typing import List, Tuple


class Direction(enum.Enum):
    NONE = 0
    HORIZONTAL = 1
    VERTICAL = 2


class Point:
    def __init__(self, point_data: Tuple[int, int]):
        self.x: int = point_data[0]
        self.y: int = point_data[1]


def get_start_and_end_nodes(point_a: Point, point_b: Point, variable: str) -> Tuple[int, int]:
    if getattr(point_a, variable) < getattr(point_b, variable):
        start = getattr(point_a, variable)
        end = getattr(point_b, variable)
    else:
        start = getattr(point_b, variable)
        end = getattr(point_a, variable)
    return start, end


class Diagram:
    def __init__(self, paths: List[Tuple[Point, Point]]):
        self.paths: List[Tuple[Point, Point]] = paths
        self.grid: List[List[int]] = self.populate_base_map()

    def populate_base_map(self) -> List[List[int]]:
        max_x = max([max([point.x for point in point_tuples]) for point_tuples in self.paths])
        max_y = max([max([point.y for point in point_tuples]) for point_tuples in self.paths])
        nested_list_size = max(max_x, max_y) + 1
        return [[0] * nested_list_size for i in range(nested_list_size)]

    def plot_vents(self):
        for path in self.paths:
            self.plot_path(path)

    def plot_horizontal_path(self, point_a: Point, point_b: Point):
        start_x, end_x = get_start_and_end_nodes(point_a, point_b, 'x')
        y = point_a.y
        for x in range(start_x, end_x + 1):
            self.grid[y][x] += 1

    def plot_vertical_path(self, point_a: Point, point_b: Point):
        x = point_a.x
        start_y, end_y = get_start_and_end_nodes(point_a, point_b, 'y')
        for y in range(start_y, end_y + 1):
            self.grid[y][x] += 1

    def plot_diagonal_path(self, point_a: Point, point_b: Point):
        x_up: bool = point_a.x < point_b.x
        y_up: bool = point_a.y < point_b.y
        x = point_a.x
        y = point_a.y
        self.grid[y][x] += 1
        while y != point_b.y and x != point_b.x:
            x += 1 if x_up else -1
            y += 1 if y_up else -1
            self.grid[y][x] += 1

    def plot_path(self, path: Tuple[Point, Point]):
        point_a, point_b = path
        if point_a.y == point_b.y:
            self.plot_horizontal_path(point_a, point_b)
        elif point_a.x == point_b.x:
            self.plot_vertical_path(point_a, point_b)
        elif abs(point_a.x - point_b.x) == abs(point_a.y - point_b.y):
            self.plot_diagonal_path(point_a, point_b)

    def calculate_number_of_dangerous_points(self, danger_level: int) -> int:
        return len([x for row in self.grid for x in row if x >= danger_level])


def main(file_path: Path):
    with open(file_path) as file:
        lines = [x.rstrip() for x in file.readlines()]
    path_list: List[Tuple[Point, Point]] = []
    for line in lines:
        point_a, point_b = line.split(' -> ')
        point_a = point_a.split(',')
        point_b = point_b.split(',')
        first_point = Point((int(point_a[0]), int(point_a[1])))
        second_point = Point((int(point_b[0]), int(point_b[1])))
        path_list.append((first_point, second_point))

    diagram = Diagram(path_list)
    diagram.plot_vents()
    danger_points = diagram.calculate_number_of_dangerous_points(2)

    print(f'Number of Danger Points: {danger_points}')


if __name__ == '__main__':
    p = Path('../input/day5_1.txt')
    main(p)
