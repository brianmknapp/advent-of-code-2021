from pathlib import Path
from typing import List, Tuple, Optional


class SevenSegmentNumber:
    def __init__(self, value: str):
        self.value = value

    def get_integer_value(self) -> Optional[int]:
        segments = len(self.value)
        if segments == 2:
            return 1
        elif segments == 3:
            return 7
        elif segments == 4:
            return 4
        elif segments == 7:
            return 8
        else:
            return None



class FourDigitOutput:
    def __init__(self, input_data: List[str]):
        self.data: List[SevenSegmentNumber] = [SevenSegmentNumber(x) for x in input_data]


class UniqueSignalPattern:
    def __init__(self, input_data: List[str]):
        self.data: List[SevenSegmentNumber] = [SevenSegmentNumber(x) for x in input_data]


class Display:
    def __init__(self, input_data: List[Tuple[List[str], List[str]]]):
        self.data: List[Tuple[UniqueSignalPattern, FourDigitOutput]] = [
            (UniqueSignalPattern(data_tuple[0]), FourDigitOutput(data_tuple[1])) for data_tuple in input_data]

    def count_four_digit_output_easy_values(self) -> int:
        result: int = 0
        for data in self.data:
            four_digit_output = data[1]
            for digit in four_digit_output.data:
                if digit.get_integer_value():
                    result += 1
        return result


def main(file_path: Path):
    with open(file_path) as file:
        lines = [x.rstrip().split('|') for x in file.readlines()]
    input_data: List[Tuple[List[str], List[str]]] = [(line[0].split(), line[1].split()) for line in lines]
    display = Display(input_data)
    result = display.count_four_digit_output_easy_values()
    print(f'Easy Mode: {result}')


if __name__ == '__main__':
    p = Path('../input/day8_test.txt')
    main(p)

    p = Path('../input/day8_1.txt')
    main(p)
