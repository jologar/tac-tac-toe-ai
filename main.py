from typing import Callable
from ai import AiConfig, AiEvaluationValues, MinMaxAi
from game import Game, GameState
from board import Board, TileValue
from gameui import tkinterui as tkui

class AiCallbackWrapper:
    def __init__(self, callback: Callable):
        self.__callback = callback
    def callback(self):
        result = self.__callback()
        if result == GameState.DRAW:
            return AiEvaluationValues.DRAW
        if result == GameState.VICTORY_O:
            return AiEvaluationValues.VICTORY_1
        if result == GameState.VICTORY_X:
            return AiEvaluationValues.VICTORY_2
        if result == GameState.ONGOING:
            return AiEvaluationValues.ONGOING    

def main():
    board = Board()
    game = Game(board)
    # TODO: Refactor AI initialization implementing it in the correct place
    # AI initialization
    aiCallbackWrapper = AiCallbackWrapper(game.game_state)
    aiConfig = AiConfig(TileValue.O.value, TileValue.X.value, TileValue.EMPTY.value, aiCallbackWrapper.callback)
    ai = MinMaxAi(aiConfig)

    # ui = ConsoleUi(game, ai)
    ui = tkui.TkinterGui(game, ai)
    ui.start()

if __name__ == "__main__":
    main()
