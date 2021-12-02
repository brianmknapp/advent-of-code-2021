from pathlib import Path
from typing import List


def calculate_three_measurement_window_increases(depths: List[int]) -> int:
    sums: List[int] = []
    n_minus_1: int = None
    n_minus_2: int = None
    for depth in depths:
        if n_minus_1 is not None and n_minus_2 is not None:
            sums.append(depth + n_minus_1 + n_minus_2)
        n_minus_2 = n_minus_1
        n_minus_1 = depth

    return calculate_depth_measurement_increases(sums)


def calculate_depth_measurement_increases(depths: List[int]) -> int:
    previous: int = None
    increases: int = 0
    for depth in depths:
        if previous is not None:
            if depth > previous:
                increases += 1
        previous = depth

    return increases


def main(file_path: Path):
    with open(file_path) as file:
        lines = file.readlines()
        lines = [int(line.rstrip()) for line in lines]

    larger_measurements = calculate_depth_measurement_increases(lines)
    print(f'Larger Measurements: {larger_measurements}')

    larger_three_window_measurements = calculate_three_measurement_window_increases(lines)
    print(f'Larger Three-Window Measurements: {larger_three_window_measurements}')


if __name__ == '__main__':
    p = Path('../input/day1_1.txt')
    main(p)
