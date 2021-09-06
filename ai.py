
from enum import Enum
from typing import Callable, List
import random

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

MAX_INIT = -1000
MIN_INIT = 1000
MAX_SCORE = 10
MIN_SCORE = -10
DRAW_SCORE = 10

class MinMaxAi(GameAi):
    maxPlayer: str
    def __init__(self, config: AiConfig):
        super().__init__(config)
        self.__max_score = MAX_SCORE
        self.__min_score = MIN_SCORE
        self.__draw_score = DRAW_SCORE

    def __is_max_player(self, player: str):
        return self.maxPlayer == player

    def __get_oponent_player(self, player: str):
        return self.config.player1 if self.config.player2 == player else self.config.player2
    
    def minmax(self, board: List, depth: int, player: str, alpha: int, beta: int):
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
            bestScore = MAX_INIT
            for idx, tile in enumerate(board):
                if tile == self.config.emptyValue:
                    board[idx] = player
                    nextPlayer = self.__get_oponent_player(player)
                    bestScore = max(bestScore, self.minmax(board, depth + 1, nextPlayer, alpha, beta))
                    # Undo the move
                    board[idx] = self.config.emptyValue
                    # Prunning
                    alpha = max(alpha, bestScore)
                    if beta <= alpha:
                        break

            return bestScore
        else:
            # Process minmax if MIN player turn
            bestScore = MIN_INIT
            for idx, tile in enumerate(board):
                if tile == self.config.emptyValue:
                    board[idx] = player
                    nextPlayer = self.__get_oponent_player(player)
                    bestScore = min(bestScore, self.minmax(board, depth + 1, nextPlayer, alpha, beta))
                    # Undo the move
                    board[idx] = self.config.emptyValue
                    #Prunning
                    beta = min(beta, bestScore)
                    if beta <= alpha:
                        break

            return bestScore


    def getPlayerMove(self, player: str, board: List):
        super().getPlayerMove(player, board)
        bestScore = MAX_INIT
        bestMoves = []
        self.maxPlayer = player

        for idx, tile in enumerate(board):
            # Check if tile is empty
            if tile == self.config.emptyValue:
                board[idx] = player
                score = self.minmax(board, 0, self.__get_oponent_player(player), MAX_INIT, MIN_INIT)
                # Undo the move
                board[idx] = self.config.emptyValue
                # set best score and best move
                if score > bestScore:
                    bestMoves = []
                    bestScore = score
                    bestMoves.append((idx, score))
                elif score == bestScore:
                    bestMoves.append((idx, score))
        # Randomize best move between the pairs
        bestMove = bestMoves[random.randint(0, len(bestMoves) - 1)]

        return bestMove[0]



