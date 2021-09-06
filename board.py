from typing import List
from enum import Enum

class TileValue(Enum):
    O = 'O'
    X = 'X'
    EMPTY = '-'

class Board:
    def __init__(self):
        self._board: List = []
        # self._board: List = ['O', 'X', 'O', '-', 'X', '-', '-', '-', '-']
        for n in range(9):
            self._board.append(TileValue.EMPTY.value)

    def __transformIndex(self, row: int, col: int):
        return (row * 3) + col

    def get_board_state(self):
        return self._board
    
    def set_tile_value(self, row: int, col: int, value: TileValue):
        if not self.is_valid_tile(row, col):
            raise ValueError
        self._board[self.__transformIndex(row, col)] = value.value

    def get_tile(self, row, col):
        if not self.is_valid_tile(row, col):
            raise ValueError
        return self._board[self.__transformIndex(row, col)]

    def is_valid_tile(self, row: int, col: int):
        return (0 <= row <= 2) and (0 <= col <= 2)

    def is_empty_tile(self, row: int, col: int):
        if not self.is_valid_tile(row, col):
            raise ValueError
        idx = self.__transformIndex(row, col)
        return self._board[idx] == TileValue.EMPTY.value

    def reset_board(self):
        for idx in range(len(self._board)):
            self._board[idx] = TileValue.EMPTY.value
