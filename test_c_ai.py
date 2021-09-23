from main import AiCallbackWrapper
from game import Game
from ai import AiConfig, FastMinMaxAi
from board import TileValue, Board

testBoard = Board()
game = Game(testBoard)

aiConfig = AiConfig(TileValue.O.value, TileValue.X.value, TileValue.EMPTY.value, lambda board: print(board))
ai = FastMinMaxAi(aiConfig)

print(ai.getPlayerMove(TileValue.O.value, testBoard.get_board_state()))
