from itertools import permutations
from pathlib import Path
from typing import List, Tuple, Optional, Dict


def valid_wire_configuration(wires: List[str], signal_patterns: List[str]) -> bool:
    known_bits: Dict[int, Optional[str]] = {i: wires[i] for i in range(7)}
    for signal_pattern in signal_patterns:
        value, known_bits = get_known_integer_value(signal_pattern, known_bits)
        if not isinstance(value, int):
            return False
    return True


def get_known_integer_value(value: str, known_bits: Dict[int, Optional[str]]) -> Tuple[Optional[int], Dict[int, str]]:
    segments = len(value)
    result = None
    if segments == 2:
        if all([known_bits[i] in value for i in [2, 5]]):
            result = 1
    if segments == 3:
        if all([known_bits[i] in value for i in [0, 2, 5]]):
            result = 7
    if segments == 4:
        if all([known_bits[i] in value for i in [1, 2, 3, 5]]):
            result = 4
    if segments == 5:
        if all([known_bits[i] in value for i in [0, 2, 3, 4, 6]]):
            result = 2
        if all([known_bits[i] in value for i in [0, 2, 3, 5, 6]]):
            result = 3
        if all([known_bits[i] in value for i in [0, 1, 3, 5, 6]]):
            result = 5
    if segments == 6:
        if all([known_bits[i] in value for i in [0, 1, 2, 4, 5, 6]]):
            result = 0
        if all([known_bits[i] in value for i in [0, 1, 3, 4, 5, 6]]):
            result = 6
        if all([known_bits[i] in value for i in [0, 1, 2, 3, 5, 6]]):
            result = 9
    if segments == 7:
        if all([known_bits[i] in value for i in range(segments)]):
            result = 8
    return result, known_bits


def get_integer_value(value: str, known_bits: Dict[int, Optional[str]]) -> Tuple[Optional[int], Dict[int, str]]:
    segments = len(value)
    if segments == 2:
        if known_bits[2] and known_bits[5]:
            if known_bits[2] in value and known_bits[5] in value:
                return 1, known_bits
        return 1, known_bits
    elif segments == 3:
        return 7, known_bits
    elif segments == 4:
        return 4, known_bits
    elif segments == 5:
        return None, known_bits
    elif segments == 6:
        return None, known_bits
    elif segments == 7:
        return 8, known_bits
    else:
        return None, known_bits


class SevenSegmentNumber:
    def __init__(self, value: str):
        self.value: str = value
        self.integer_value: Optional[int] = None


class FourDigitOutput:
    def __init__(self, input_data: List[str]):
        self.data: List[SevenSegmentNumber] = [SevenSegmentNumber(x) for x in input_data]
        self.digits: Optional[str] = None


class UniqueSignalPattern:
    def __init__(self, input_data: List[str]):
        self.data: List[SevenSegmentNumber] = [SevenSegmentNumber(x) for x in input_data]
        self.digits: Optional[str] = None


class SingleDisplay:
    def __init__(self, input_data: Tuple[List[str], List[str]]):
        self.unique_signal_patterns: UniqueSignalPattern = UniqueSignalPattern(input_data[0])
        self.four_digit_outputs: FourDigitOutput = FourDigitOutput(input_data[1])
        self.patterns_display_data: Dict[str, Optional[int]] = {k: None for k in set([''.join(x.value) for x in self.unique_signal_patterns.data])}
        self.outputs_display_data: Dict[str, Optional[int]] = {k: None for k in [''.join(x.value) for x in self.four_digit_outputs.data]}
        self.known_bits: Dict[int, str] = {i: None for i in range(1, 8)}

    def parse_display(self):
        for k in self.patterns_display_data.keys():
            value, self.known_bits = get_integer_value(k, self.known_bits)
            if value:
                self.patterns_display_data[k] = value
        for k in self.outputs_display_data.keys():
            value, self.known_bits = get_integer_value(k, self.known_bits)
            if value:
                self.outputs_display_data[k] = value

    def find_valid_wire_combination(self) -> Optional[List[str]]:
        working_list = [x for x in 'abcdefg']
        combos: List[List[str]] = [list(x) for x in permutations(working_list, len(working_list))]
        for combo in combos:
            validity = valid_wire_configuration(combo, [k for k in self.patterns_display_data.keys()])
            if validity:
                self.known_bits = {i: combo[i] for i in range(7)}
                for i in range(len(self.unique_signal_patterns.data)):
                    self.unique_signal_patterns.data[i].integer_value = get_known_integer_value(self.unique_signal_patterns.data[i].value, self.known_bits)[0]
                return combo
        return None

    def find_output_value(self):
        for i in range(len(self.four_digit_outputs.data)):
            self.four_digit_outputs.data[i].integer_value = get_known_integer_value(self.four_digit_outputs.data[i].value, self.known_bits)[0]



class Display:
    def __init__(self, input_data: List[Tuple[List[str], List[str]]]):
        self.data: List[SingleDisplay] = [SingleDisplay(data_tuple) for data_tuple in input_data]

    def count_four_digit_output_easy_values(self) -> int:
        result: int = 0
        for single_display in self.data:
            four_digit_output = single_display.four_digit_outputs
            for digit in four_digit_output.data:
                digit_value, single_display.known_bits = get_integer_value(digit.value, single_display.known_bits)
                if digit_value:
                    result += 1
        return result

    def part_2(self) -> int:
        result: int = 0
        for single_display in self.data:
            single_display.parse_display()
            valid_combo = single_display.find_valid_wire_combination()
            if valid_combo:
                single_display.find_output_value()
            single_display.unique_signal_patterns.digits = ''.join(str(x.integer_value) for x in single_display.unique_signal_patterns.data)
            single_display.four_digit_outputs.digits = ''.join(str(x.integer_value) for x in single_display.four_digit_outputs.data)
            result += int(single_display.four_digit_outputs.digits)
        return result


def main(file_path: Path):
    with open(file_path) as file:
        lines = [x.rstrip().split('|') for x in file.readlines()]
    input_data: List[Tuple[List[str], List[str]]] = [(line[0].split(), line[1].split()) for line in lines]
    display = Display(input_data)
    result = display.count_four_digit_output_easy_values()
    print(f'Easy Mode: {result}')

    result = display.part_2()
    print(f'Part II: {result}')


if __name__ == '__main__':
    p = Path('../input/day8_simple.txt')
    main(p)

    p = Path('../input/day8_test.txt')
    main(p)

    p = Path('../input/day8_1.txt')
    main(p)
