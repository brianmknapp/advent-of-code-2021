import sys
from math import prod
from pathlib import Path
from typing import List, Tuple

MAX_INT = sys.maxsize


class Heatmap:
    def __init__(self, input_data: List[List[int]]):
        self.input_data = input_data
        self.last_column = len(self.input_data[0]) - 1
        self.last_row = len(self.input_data) - 1
        self.low_points: List[Tuple[int, int]] = []
        self.risk_values: List[int] = []
        self.basin_map = self.input_data
        self.basin_sizes: List[int] = []

    def find_low_points(self):
        for i, x in enumerate(self.input_data):
            for j, y in enumerate(x):
                up = self.input_data[i - 1][j] if i > 0 else MAX_INT
                down = self.input_data[i + 1][j] if i < self.last_row else MAX_INT
                left = self.input_data[i][j - 1] if j > 0 else MAX_INT
                right = self.input_data[i][j + 1] if j < self.last_column else MAX_INT
                if all([y < v for v in [up, down, left, right]]):
                    self.low_points.append((i, j))
                    self.risk_values.append(y + 1)

    def find_basins(self):
        for low_point in self.low_points:
            basin_size = self.traverse_basin(low_point)
            self.basin_sizes.append(basin_size)

    def traverse_basin(self, node: Tuple[int, int], visited_nodes=None):
        if visited_nodes is None:
            visited_nodes = []
        if node in visited_nodes:
            return 0
        i, j = node
        count = 0
        up = (i - 1, j) if i > 0 else None
        down = (i + 1, j) if i < self.last_row else None
        left = (i, j - 1) if j > 0 else None
        right = (i, j + 1) if j < self.last_column else None
        adjacent_nodes = [up, down, left, right]
        if self.basin_map[i][j] == 9:
            return 0
        visited_nodes.append(node)
        count += 1
        for adjacent_node in adjacent_nodes:
            if adjacent_node:
                count += self.traverse_basin(adjacent_node, visited_nodes)
        return count


def main(file_path: Path):
    with open(file_path) as file:
        lines = [x.rstrip() for x in file.readlines()]
    data = [[int(x) for x in line] for line in lines]
    heatmap = Heatmap(data)
    heatmap.find_low_points()
    risk_values_sum = sum(heatmap.risk_values)
    print(f'Risk Value Sum: {risk_values_sum}')

    heatmap.find_basins()
    largest_three_basins = sorted(heatmap.basin_sizes)[-3:]
    print(f'Largest Three Basins: {largest_three_basins[0]} * {largest_three_basins[1]} * {largest_three_basins[2]} = {prod(largest_three_basins)}')


if __name__ == '__main__':
    p = Path('../input/day9_test.txt')
    main(p)

    p = Path('../input/day9_1.txt')
    main(p)
