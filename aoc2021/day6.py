from pathlib import Path
from typing import List, Dict


class BreedingCalculator:
    def __init__(self, existing_fish: List[int]):
        self.original_laternfish: Dict[int, int] = self.get_initial_collection(existing_fish)
        self.current_laternfish: Dict[int, int] = {}
        
    def get_initial_collection(self, existing_fish: List[int]) -> Dict[int, int]:
        result: Dict[int, int] = {}
        for i in range(9):
            fish_count = len([x for x in existing_fish if x == i])
            result[i] = fish_count
        return result

    def progress_days(self, days_to_progress: int) -> int:
        self.current_laternfish = self.original_laternfish
        for i in range(1, days_to_progress + 1):
            fish_to_breed = self.current_laternfish[0]
            self.current_laternfish[0] = self.current_laternfish[1]
            self.current_laternfish[1] = self.current_laternfish[2]
            self.current_laternfish[2] = self.current_laternfish[3]
            self.current_laternfish[3] = self.current_laternfish[4]
            self.current_laternfish[4] = self.current_laternfish[5]
            self.current_laternfish[5] = self.current_laternfish[6]
            self.current_laternfish[6] = self.current_laternfish[7] + fish_to_breed
            self.current_laternfish[7] = self.current_laternfish[8]
            self.current_laternfish[8] = fish_to_breed
        return sum({v for (k, v) in self.current_laternfish.items()})


def main(file_path: Path, days_to_progress: int):
    with open(file_path) as file:
        line = file.readline()
        input_data = [int(x) for x in line.split(',')]

    breeding_calculator = BreedingCalculator(input_data)
    count_after_days = breeding_calculator.progress_days(days_to_progress)

    print(f'Count after {days_to_progress} days: {count_after_days}')


if __name__ == '__main__':
    p = Path('../input/day6_test.txt')
    main(p, 256)

    p = Path('../input/day6_1.txt')
    main(p, 256)
