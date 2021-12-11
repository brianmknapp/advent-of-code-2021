from pathlib import Path
from typing import List, Tuple, Optional

from pandas import DataFrame


class Octopus:
    def __init__(self, energy_level: int):
        self.energy_level = energy_level
        self.flashed: bool = False

    def increase_energy_level(self) -> int:
        self.energy_level += 1
        return self.energy_level


class Submarine:
    def __init__(self, octopi: List[List[Octopus]], steps: int = 100, debug: bool = False):
        self.octopi = octopi
        self.debug = debug
        self.simultaneously_flashed: List[int] = []
        self.total_flashes_after_steps = self.model_energy_levels(steps)

    def model_energy_levels(self, steps: int) -> int:
        flashes = 0
        if self.debug:
            print('Before Any Steps:')
            print(DataFrame([[octopus.energy_level for octopus in octopi] for octopi in self.octopi]))
        for step in range(steps):
            octopi_to_flash = self.increase_energy_level()
            octopi_that_flashed = self.flash_octopi(octopi_to_flash)
            if all([octopus.flashed for octopi in self.octopi for octopus in octopi]):
                self.simultaneously_flashed.append(step + 1)
            self.reset_energy_levels_for_flashed_octopi(octopi_that_flashed)
            if self.debug:
                print(f'\nAfter Step {step + 1}:')
                print(DataFrame([[octopus.energy_level for octopus in octopi] for octopi in self.octopi]))
            flashes += len(octopi_that_flashed)

        return flashes

    def increase_energy_level(self) -> List[Tuple[int, int]]:
        octopi_to_flash: List[Tuple[int, int]] = []
        for i, row in enumerate(self.octopi):
            for j, cell in enumerate(row):
                new_energy_level = self.octopi[i][j].increase_energy_level()
                if new_energy_level > 9:
                    octopi_to_flash.append((i, j))

        return octopi_to_flash

    def flash_octopi(self, octopi_to_flash: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        octopi_that_flashed: List[Tuple[int, int]] = []
        for octopi in octopi_to_flash:
            i, j = octopi
            result = self.flash_octopus((i, j), octopi_that_flashed)
            octopi_that_flashed = result

        return octopi_that_flashed

    def flash_octopus(self, octopus_pos: Tuple[int, int], octopi_that_flashed: List[Tuple[int, int]] = None) -> List[Tuple[int, int]]:
        if octopi_that_flashed is None:
            octopi_that_flashed = []

        i, j = octopus_pos

        if (i, j) in octopi_that_flashed:
            return octopi_that_flashed

        go_north: bool = i > 0
        go_west: bool = j > 0
        go_east: bool = j < len(self.octopi[0]) - 1
        go_south: bool = i < len(self.octopi) - 1
        nw: Optional[Tuple[int, int]] = (i - 1, j - 1) if all([go_north, go_west]) else None
        n: Optional[Tuple[int, int]] = (i - 1, j) if go_north else None
        ne: Optional[Tuple[int, int]] = (i - 1, j + 1) if all([go_north, go_east]) else None
        w: Optional[Tuple[int, int]] = (i, j - 1) if go_west else None
        e: Optional[Tuple[int, int]] = (i, j + 1) if go_east else None
        sw: Optional[Tuple[int, int]] = (i + 1, j - 1) if all([go_south, go_west]) else None
        s: Optional[Tuple[int, int]] = (i + 1, j) if go_south else None
        se: Optional[Tuple[int, int]] = (i + 1, j + 1) if all([go_south, go_east]) else None

        self.octopi[i][j].flashed = True
        octopi_that_flashed.append((i, j))

        for adjacent_octopus_pos in [direction for direction in [nw, n, ne, w, e, sw, s, se] if direction is not None]:
            x, y = adjacent_octopus_pos
            new_energy_level = self.octopi[x][y].increase_energy_level()
            if new_energy_level > 9:
                self.flash_octopus((x, y), octopi_that_flashed)

        return octopi_that_flashed

    def reset_energy_levels_for_flashed_octopi(self, octopi_that_flashed: List[Tuple[int, int]]):
        for octopi in octopi_that_flashed:
            i, j = octopi
            self.octopi[i][j].energy_level = 0
            self.octopi[i][j].flashed = False


def main(file_path: Path, steps: int = 100, debug: bool = False):
    with open(file_path) as file:
        lines = file.readlines()
    input_data = [[Octopus(int(x)) for x in line.rstrip()] for line in lines]
    submarine = Submarine(input_data, steps, debug)
    print(f'Total Flashes: {submarine.total_flashes_after_steps}')
    print(f'First Simultaneous Flash Step: {submarine.simultaneously_flashed[0] if len(submarine.simultaneously_flashed) > 0 else None}')


if __name__ == '__main__':
    p = Path('../input/day11_simple.txt')
    main(p, 2)

    p = Path('../input/day11_test.txt')
    main(p, 1000)

    p = Path('../input/day11_1.txt')
    main(p, 1000)
