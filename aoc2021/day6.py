from pathlib import Path
from typing import List


class Laternfish:
    def __init__(self, days_until_spawn: int = 8):
        self.days_until_spawn: int = days_until_spawn


class BreedingCalculator:
    def __init__(self, existing_fish: List[int]):
        self.original_laternfish: List[Laternfish] = [Laternfish(x) for x in existing_fish]
        self.current_laternfish: List[Laternfish] = self.original_laternfish

    def progress_days(self, days_to_progress: int) -> int:
        self.current_laternfish = self.original_laternfish
        for i in range(1, days_to_progress + 1):
            new_laternfish: List[Laternfish] = []
            for laternfish in self.current_laternfish:
                if laternfish.days_until_spawn == 0:
                    laternfish.days_until_spawn = 6
                    new_laternfish.append(Laternfish(8))
                else:
                    laternfish.days_until_spawn -= 1
            self.current_laternfish.extend(new_laternfish)
            print(f'Day {i} fish: {[x.days_until_spawn for x in self.current_laternfish]} - Count: {len(self.current_laternfish)}')

        return len(self.current_laternfish)


def main(file_path: Path, days_to_progress: int):
    with open(file_path) as file:
        line = file.readline()
        input_data = [int(x) for x in line.split(',')]

    breeding_calculator = BreedingCalculator(input_data)
    count_after_days = breeding_calculator.progress_days(days_to_progress)

    print(f'Count after {days_to_progress} days: {count_after_days}')


if __name__ == '__main__':
    p = Path('../input/day6_test.txt')
    main(p, 18)

    p = Path('../input/day6_1.txt')
    #
