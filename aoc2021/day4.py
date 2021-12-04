from pathlib import Path
from typing import List, Tuple


class Board:
    def __init__(self):
        self.board_data: List[List[Tuple[int, bool]]] = []
        self.winner: bool = False

    def add_row(self, row_data: List[int]):
        self.board_data.append([(x, False) for x in row_data])

    def check_if_winner(self):
        self.winner = any([self.check_rows(), self.check_columns()])

    def check_rows(self) -> bool:
        return any([all([y for x, y in row]) for row in self.board_data])

    def check_columns(self) -> bool:
        data: List[bool] = []
        for j in range(len(self.board_data[0])):
            column_data: List[bool] = []
            for i in range(len(self.board_data)):
                column_data.append(self.board_data[i][j][1])
            data.append(all(column_data))
        return any(data)

    def calculate_score(self, last_called_value: int) -> int:
        score: int = 0
        for row in self.board_data:
            for col in row:
                col_val, matched = col
                if not matched:
                    score += col_val
        return score * last_called_value


class Game:
    def __init__(self, game_data: List[int], boards: List[Board]):
        self.game_data = game_data
        self.boards = boards

    def call_number(self, number: int):
        for board in self.boards:
            for i, row in enumerate(board.board_data):
                for j, cell in enumerate(row):
                    cell_value, matched = cell
                    if cell_value == number:
                        board.board_data[i][j] = (cell_value, True)
            board.check_if_winner()

    def check_for_winner(self) -> Board or None:
        for board in self.boards:
            if board.winner:
                return board
        return None


def main(file_path: Path):
    with open(file_path) as file:
        data = [x.rstrip() for x in file.readlines()]
    game_data: List[int] = [int(x) for x in data[0].split(',')]
    boards: List[Board] = []

    current_board = Board()
    for i, line in enumerate(data):
        if 0 <= i <= 1:
            continue
        if not line or i == len(data) - 1:
            boards.append(current_board)
            current_board = Board()
        else:
            current_board.add_row([int(x) for x in line.split()])

    game = Game(game_data, boards)
    for number in game.game_data:
        game.call_number(number)
        winner = game.check_for_winner()
        if winner:
            print(f'Winning Board Value: {winner.calculate_score(number)}')
            break


if __name__ == '__main__':
    p = Path('../input/day4_1.txt')
    main(p)
