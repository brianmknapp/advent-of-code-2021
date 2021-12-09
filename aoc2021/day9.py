import sys
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


def main(file_path: Path):
    with open(file_path) as file:
        lines = [x.rstrip() for x in file.readlines()]
    data = [[int(x) for x in line] for line in lines]
    heatmap = Heatmap(data)
    heatmap.find_low_points()
    risk_values_sum = sum(heatmap.risk_values)
    print('bagel')


if __name__ == '__main__':
    p = Path('../input/day9_test.txt')
    main(p)

    p = Path('../input/day9_1.txt')
    main(p)
