from pathlib import Path
from typing import Dict, Optional, List


POINTS: Dict[str, int] = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

OPENERS_CLOSERS: Dict[str, str] = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>'
}

OPENERS: List[str] = [x for x in OPENERS_CLOSERS.keys()]

CLOSERS: List[str] = [x for x in OPENERS_CLOSERS.values()]


class Chunk:
    def __init__(self, chunk_data: str):
        self.chunk_data: List[str] = [x for x in chunk_data]
        self.first_incorrect_closing_character: Optional[str] = self.find_first_incorrect_closing_character()

    def find_first_incorrect_closing_character(self, openers_stack: List[str] = None, current_index: int = 0):
        if current_index == len(self.chunk_data):
            return None

        if openers_stack is None:
            openers_stack = []

        value = self.chunk_data[current_index]

        if value in CLOSERS:
            if value != OPENERS_CLOSERS[openers_stack[-1]]:
                return value
            openers_stack.pop()

        if value in OPENERS:
            openers_stack.append(value)

        current_index += 1
        return self.find_first_incorrect_closing_character(openers_stack, current_index)


def main(file_path: Path):
    with open(file_path) as file:
        lines = [x.rstrip() for x in file.readlines()]

    chunks = [Chunk(x) for x in lines]
    chunk_values = sum([POINTS[chunk.first_incorrect_closing_character] for chunk in chunks if chunk.first_incorrect_closing_character is not None])
    print(f'Total Syntax Error Sum: {chunk_values}')


if __name__ == '__main__':
    p = Path('../input/day10_test.txt')
    main(p)

    p = Path('../input/day10_1.txt')
    main(p)
