from ai import AiConfig, FastMinMaxAi
from board import TileValue

aiConfig = AiConfig(TileValue.O.value, TileValue.X.value, TileValue.EMPTY.value, lambda : "T")
ai = FastMinMaxAi(aiConfig)
print(ai.getPlayerMove(TileValue.O.value, []))