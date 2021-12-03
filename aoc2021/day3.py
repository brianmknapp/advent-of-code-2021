from pathlib import Path
from typing import List


def calculate_power_consumption(data: List[List[str]]) -> int:
    gamma_rate = int(calculate_gamma_rate(data), 2)
    epsilon_rate = int(calculate_epsilon_rate(data), 2)
    print(f'Gamma Rate: {gamma_rate}')
    print(f'Epsilon Rate: {epsilon_rate}')
    return gamma_rate * epsilon_rate


def calculate_gamma_rate(data: List[List[str]]) -> str:
    gamma_rate: str = ''
    for j in range(len(data[0])):
        off_count = 0
        on_count = 0
        for row in data:
            pos_value = row[j]
            if pos_value == '0':
                off_count += 1
            if pos_value == '1':
                on_count += 1
            else:
                continue
        gamma_rate = gamma_rate + ('1' if on_count > off_count else '0')

    return gamma_rate


def calculate_epsilon_rate(data: List[List[str]]) -> str:
    epsilon_rate: str = ''
    for j in range(len(data[0])):
        off_count = 0
        on_count = 0
        for i, row in enumerate(data):
            pos_value = row[j]
            if pos_value == '0':
                off_count += 1
            if pos_value == '1':
                on_count += 1
            else:
                continue
        epsilon_rate = epsilon_rate + ('1' if on_count < off_count else '0')

    return epsilon_rate


def main(file_path: Path):
    with open(file_path) as file:
        lines = file.readlines()
        input_data: List[List[str]] = [[x for x in line.rstrip()] for line in lines]

    power_consumption = calculate_power_consumption(input_data)
    print(f'Power Consumption: {power_consumption}')


if __name__ == '__main__':
    p = Path('../input/day3_1.txt')
    main(p)
