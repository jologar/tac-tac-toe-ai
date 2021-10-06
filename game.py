from observable import Observable
from board import Board, TileValue
from enum import Enum

class Player(Enum):
    PLAYER_1 = TileValue.O.value
    PLAYER_2 = TileValue.X.value

class GameState(Enum):
    DRAW = 0
    VICTORY_O = 1
    VICTORY_X = 2
    ONGOING = 3

class NotEmptyTile(Exception):
    pass

def victory_line(first: str, second: str, third: str):
    if (first != TileValue.EMPTY.value) and (first == second) and (second == third):
        return GameState.VICTORY_O if TileValue.O.value == first else GameState.VICTORY_X
    return False

RANGE = 3

class Game(Observable):
    def __init__(self, board: Board):
        super().__init__()
        self.__board = board
        self.__player_turn = Player.PLAYER_1
        self.__human = set()

    def __check_victory_in_row(self, row: int):
        first = self.__board.get_tile(row, 0)
        second = self.__board.get_tile(row, 1)
        third = self.__board.get_tile(row, 2)
        return victory_line(first, second, third)

    def __check_victory_in_column(self, column: int):
        first = self.__board.get_tile(0, column)
        second = self.__board.get_tile(1, column)
        third = self.__board.get_tile(2, column)
        return victory_line(first, second, third)

    def __check_victory_in_diagonal_right(self):
        first = self.__board.get_tile(0, 0)
        second = self.__board.get_tile(1, 1)
        third = self.__board.get_tile(2, 2)
        return victory_line(first, second, third)

    def __check_victory_in_diagonal_left(self):
        first = self.__board.get_tile(0, 2)
        second = self.__board.get_tile(1, 1)
        third = self.__board.get_tile(2, 0)
        return victory_line(first, second, third)

    def __is_draw(self):
        for row in range(RANGE):
            for col in range(RANGE):
                if self.__board.is_empty_tile(row, col):
                    return False
        return True

    def reset_game(self):
        self.__board.reset_board()
        self.__player_turn = Player.PLAYER_1
        self.fire()

    def clean_players(self):
        self.__human = set()

    def set_human(self, player: Player):
        self.__human.add(player)

    def is_human(self, player: Player):
        return player in self.__human

    def has_human_player(self):
        return len(self.__human) > 0

    def is_pvp(self):
        return len(self.__human) == 2

    def switch_turn(self):
        self.__player_turn = Player.PLAYER_2 if self.__player_turn == Player.PLAYER_1 else Player.PLAYER_1

    def do_move(self, row: int, col: int):
        if not self.__board.is_empty_tile(row, col):
            raise NotEmptyTile()
        value = TileValue.O if self.__player_turn == Player.PLAYER_1 else TileValue.X
        self.__board.set_tile_value(row, col, value)
        self.switch_turn()
        self.fire()

    def get_player_turn(self):
        return self.__player_turn

    def get_game_data(self):
        return self.__board.get_board_state()

    def game_state(self):
        for idx in range(RANGE):
            # Check victory in lines
            result = self.__check_victory_in_row(idx)
            if result != False:
                return result
            # Check victory in columns
            result = self.__check_victory_in_column(idx)
            if result != False:
                return result

        # Check victory in diagonal left
        result = self.__check_victory_in_diagonal_left()
        if result != False:
            return result
        # Check victory in diagonal right
        result = self.__check_victory_in_diagonal_right()
        if result != False:
            return result
    
        # Check if is draw
        return GameState.DRAW if self.__is_draw() else GameState.ONGOING
