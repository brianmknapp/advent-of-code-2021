from pathlib import Path
from typing import List, Tuple


def travel_submarine_with_aim(course: List[str]) -> Tuple[int, int]:
    horizontal_pos = 0
    depth = 0
    aim = 0
    for instruction in course:
        parsed_instruction = instruction.split()
        direction: str = parsed_instruction[0]
        distance: int = int(parsed_instruction[1])

        if direction == 'forward':
            horizontal_pos += distance
            if aim != 0:
                depth += distance * aim
        if direction == 'down':
            aim += distance
        if direction == 'up':
            aim -= distance
    return horizontal_pos, depth


def travel_submarine(course: List[str]) -> Tuple[int, int]:
    horizontal_pos = 0
    depth = 0
    for instruction in course:
        parsed_instruction = instruction.split()
        direction: str = parsed_instruction[0]
        distance: int = int(parsed_instruction[1])

        if direction == 'forward':
            horizontal_pos += distance
        if direction == 'down':
            depth += distance
        if direction == 'up':
            depth -= distance
    return horizontal_pos, depth


def main(file_path: Path):
    with open(file_path) as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]

    horizontal_pos, depth = travel_submarine(lines)
    print(f'Without aim: {horizontal_pos} * {depth}: {horizontal_pos * depth}')

    horizontal_pos, depth = travel_submarine_with_aim(lines)
    print(f'With aim: {horizontal_pos} * {depth}: {horizontal_pos * depth}')


if __name__ == '__main__':
    p = Path('../input/day2_1.txt')
    main(p)
