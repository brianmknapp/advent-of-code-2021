from typing import List


def calculate_depth_measurement_increases(depths: List[int]) -> int:
    previous: int = None
    increases: int = 0
    for depth in depths:
        if previous is not None:
            if depth > previous:
                increases += 1
        previous = depth

    return increases


def main(filename: str):
    with open(filename) as file:
        lines = file.readlines()
        lines = [int(line.rstrip()) for line in lines]

    larger_measurements = calculate_depth_measurement_increases(lines)
    print(f'Larger Measurements: {larger_measurements}')


if __name__ == '__main__':
    main(r'C:\repo\training\personal\advent-of-code-2021\input\day1_1.txt')