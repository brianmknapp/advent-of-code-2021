from pathlib import Path
from typing import List, Tuple


def calculate_power_consumption_and_life_support(data: List[List[str]]) -> Tuple[int, int]:
    gamma_rate = int(calculate_gamma_rate(data), 2)
    epsilon_rate = int(calculate_epsilon_rate(data), 2)
    oxygen_generator_rating = int(calculate_oxygen_generator_rating(data), 2)
    co2_scrubber_rating = int(calculate_co2_scrubber_rating(data), 2)

    print(f'Gamma Rate: {gamma_rate}')
    print(f'Epsilon Rate: {epsilon_rate}')
    print(f'Oxygen Generator Rating: {oxygen_generator_rating}')
    print(f'CO2 Scrubber Rating: {co2_scrubber_rating}')

    return gamma_rate * epsilon_rate, oxygen_generator_rating * co2_scrubber_rating


def calculate_oxygen_generator_rating(data: [List[List[str]]]) -> str:
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
        max_count = '1' if on_count >= off_count else '0'
        data = [x for x in data if x[j] == max_count]
        if len(data) == 1:
            break
    oxygen_generator_rating = ''.join(data[0])
    return oxygen_generator_rating


def calculate_co2_scrubber_rating(data: [List[List[str]]]) -> str:
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
        min_count = '1' if on_count < off_count else '0'
        data = [x for x in data if x[j] == min_count]
        if len(data) == 1:
            break
    co2_scrubber_rating = ''.join(data[0])
    return co2_scrubber_rating


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

    power_consumption, life_support_rating = calculate_power_consumption_and_life_support(input_data)
    print(f'Power Consumption: {power_consumption}')
    print(f'Life Support Rating: {life_support_rating}')


if __name__ == '__main__':
    p = Path('../input/day3_1.txt')
    main(p)
