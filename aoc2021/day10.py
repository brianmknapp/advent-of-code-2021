import math
from pathlib import Path
from typing import Dict, Optional, List, Tuple

POINTS: Dict[str, int] = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

INCOMPLETE_POINTS: Dict[str, int] = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
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
        self.first_incorrect_closing_character, self.completion_string = self.find_first_incorrect_closing_character()
        self.incomplete_score: Optional[int] = self.calculate_incomplete_score()

    def find_first_incorrect_closing_character(self, openers_stack: List[str] = None, current_index: int = 0) -> Tuple[Optional[str], Optional[str]]:
        if current_index == len(self.chunk_data):
            openers = reversed(openers_stack)
            return None, ''.join([OPENERS_CLOSERS[x] for x in openers])

        if openers_stack is None:
            openers_stack = []

        value = self.chunk_data[current_index]

        if value in CLOSERS:
            if value != OPENERS_CLOSERS[openers_stack[-1]]:
                return value, None
            openers_stack.pop()

        if value in OPENERS:
            openers_stack.append(value)

        current_index += 1
        return self.find_first_incorrect_closing_character(openers_stack, current_index)

    def calculate_incomplete_score(self):
        if self.completion_string is None:
            return None

        score = 0
        for x in self.completion_string:
            score *= 5
            score += INCOMPLETE_POINTS[x]
        return score


def main(file_path: Path):
    with open(file_path) as file:
        lines = [x.rstrip() for x in file.readlines()]

    chunks = [Chunk(x) for x in lines]
    chunk_values = sum([POINTS[chunk.first_incorrect_closing_character] for chunk in chunks if chunk.first_incorrect_closing_character is not None])
    incomplete_chunk_values = sorted([chunk.incomplete_score for chunk in chunks if chunk.incomplete_score is not None])
    middle_value = incomplete_chunk_values[math.trunc(len(incomplete_chunk_values)/2)]
    print(f'Total Syntax Error Sum: {chunk_values}')
    print(f'Middle Incomplete Sum: {middle_value}')


if __name__ == '__main__':
    p = Path('../input/day10_test.txt')
    main(p)

    p = Path('../input/day10_1.txt')
    main(p)
