
from ai import AiConfig, FastMinMaxAi, GameAi, MinMaxAi
from main import AiCallbackWrapper
from game import Game, GameState
from board import Board, TileValue
from datetime import datetime
import random
import time

DELIMITER = ","
PROFILE_FOLDER = "./profile/"
EXTENSION = ".csv"

def profile_ai(profile_name: str, game: Game, ai: GameAi):
    game.clean_players()
    game.reset_game()
    print("Starting profiling of " + profile_name)
    # Open file buffer
    with open(PROFILE_FOLDER + profile_name + EXTENSION, "a") as file:
        profile_line = ""
        # Game loop
        while game.game_state() == GameState.ONGOING:
            move_num = 1
            player = game.get_player_turn()
            # prev timestamp
            time_start = time.process_time_ns()
            move = ai.getPlayerMove(player.value, game.get_game_data())
            # post timestamp
            time_end = time.process_time_ns()
            print("Move {0} time: {1}ns".format(move_num, time_end - time_start))
            move_time = time_end - time_start
            profile_line = profile_line + str(move_time) + DELIMITER
            move_num += 1
            # execute move to continue the game
            col = move % 3
            row = int((move - col) / 3)
            game.do_move(row, col)
            print_board(game)
        # Store profile values
        file.write(profile_line[:-1] + "\n")
        # Close the file buffer
        file.close()

def print_board(game: Game):
    line = "| "
    game_data = game.get_game_data()
    for idx, value in enumerate(game_data):
        line = line + str(value) + " "
        if (idx + 1) % 3 == 0:
            line = line + "|"
            print(line)
            line = "| "
    print('\n\n')

def evaluation():
    print("Performance evaluation program:\n")
    print("it outputs a text log with the results of both AI perfomance tests.\n")
    # Evaluates the performance of the C++ AI library, compared to the Python one.
    board = Board()
    game = Game(board)
    # Configure both AIs
    aiCallbackWrapper = AiCallbackWrapper(game.game_state)
    aiConfig = AiConfig(TileValue.O.value, TileValue.X.value, TileValue.EMPTY.value, aiCallbackWrapper.callback)
    py_ai = MinMaxAi(aiConfig)
    cpp_ai = FastMinMaxAi(aiConfig)
    # Ask user for number of test cases
    test_cases = input("Number of test cases per AI system:\n")
    now = datetime.now()
    suffix = now.strftime("%Y%m%d%H%M%S")
    for idx in range(int(test_cases)):
        # Build profile results log for Python AI
        profile_ai("python_ai_perf_{0}".format(suffix), game, py_ai)
        # Build profile results log for C++ AI
        profile_ai("cpp_ai_perf_{0}".format(suffix), game, cpp_ai)


if __name__ == "__main__":
    evaluation()