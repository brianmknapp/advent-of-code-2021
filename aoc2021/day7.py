from collections import Counter
from pathlib import Path
from typing import List, Dict


def calculate_triangular_value(count: int) -> int:
    result: int = 0
    for i in range(count):
        result += i
    return result


class CrabCollection:
    def __init__(self, initial_lineup: List[int]):
        self.lineup = initial_lineup

    def calculate_most_efficient_adjustment(self) -> Dict[int, List[int]]:
        result: Dict[int, List[int]] = {}
        for v in range(max(self.lineup)):
            result[v] = [abs(v - x) + calculate_triangular_value(abs(v - x)) for x in self.lineup]
        return result


def main(file_path: Path):
    with open(file_path) as file:
        line = file.readline()
    input_data = [int(x) for x in line.split(',')]
    crabs = CrabCollection(input_data)
    efficient_adjustments = crabs.calculate_most_efficient_adjustment()
    most_efficient = min([sum(v) for k, v in efficient_adjustments.items()])
    print(f'Most Efficient Adjustment: {most_efficient}')


if __name__ == '__main__':
    p = Path('../input/day7_test.txt')
    main(p)

    p = Path('../input/day7_1.txt')
    main(p)
