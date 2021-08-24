
from enum import Enum
from typing import Callable, List

class AiEvaluationValues(Enum):
    DRAW = 0
    VICTORY_1 = 1
    VICTORY_2 = 2
    ONGOING = 3

class AiConfig:
    def __init__(self, player1: str, player2: str, emptyValue: str, evaluation: Callable):
        self.player1 = player1
        self.player2 = player2
        self.emptyValue = emptyValue
        self.evaluationCallback = evaluation

class GameAi:
    def __init__(self, config: AiConfig):
        self.config = config

    def getPlayerMove(self, player: str, board: List):
        pass

class MinMaxAi(GameAi):
    maxPlayer: str
    def __init__(self, config: AiConfig):
        super().__init__(config)
        self.__max_score = 10
        self.__min_score = -10
        self.__draw_score = 0

    def __is_max_player(self, player: str):
        return self.maxPlayer == player

    def __get_oponent_player(self, player: str):
        return self.config.player1 if self.config.player2 == player else self.config.player2
    
    def minmax(self, board: List, depth: int, player: str, move: int):
        evalResult = self.config.evaluationCallback()
        # Check Player 1 victory
        if evalResult == AiEvaluationValues.VICTORY_1:
            minScore = self.__min_score + depth
            maxScore = self.__max_score - depth
            return maxScore if self.__is_max_player(self.config.player1) else minScore
        
        # Check Player 2 victory
        if evalResult == AiEvaluationValues.VICTORY_2:
            minScore = self.__min_score + depth
            maxScore = self.__max_score - depth
            return maxScore if self.__is_max_player(self.config.player2) else minScore

        # Check DRAW
        if evalResult == AiEvaluationValues.DRAW:
            if (self.__is_max_player(player)):
                depth = depth * -1
            return self.__draw_score + depth

        # Process minmax if MAX player turn
        if self.__is_max_player(player):
            bestScore = -1000
            for idx, tile in enumerate(board):
                if tile == self.config.emptyValue:
                    board[idx] = player
                    nextPlayer = self.__get_oponent_player(player)
                    bestScore = max(bestScore, self.minmax(board, depth + 1, nextPlayer, idx))
                    # Undo the move
                    board[idx] = self.config.emptyValue
            return bestScore
        else:
            # Process minmax if MIN player turn
            bestScore = 1000
            for idx, tile in enumerate(board):
                if tile == self.config.emptyValue:
                    board[idx] = player
                    nextPlayer = self.__get_oponent_player(player)
                    bestScore = min(bestScore, self.minmax(board, depth + 1, nextPlayer, idx))
                    # Undo the move
                    board[idx] = self.config.emptyValue
            return bestScore


    def getPlayerMove(self, player: str, board: List):
        super().getPlayerMove(player, board)
        bestMove = -1
        bestScore = -1000
        self.maxPlayer = player

        for idx, tile in enumerate(board):
            # Check if tile is empty
            if tile == self.config.emptyValue:
                board[idx] = player
                score = self.minmax(board, 0, self.__get_oponent_player(player), idx)
                # Undo the move
                board[idx] = self.config.emptyValue
                # set best score and best move
                if score > bestScore:
                    bestScore = score
                    bestMove = idx
        return bestMove



