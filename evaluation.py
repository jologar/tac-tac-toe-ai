
from ai import AiConfig, FastMinMaxAi, GameAi, MinMaxAi
from main import AiCallbackWrapper
from game import Game, GameState
from board import Board, TileValue
from datetime import datetime
import time

YES = "Y"
NO = "N"
DELIMITER = ","
PROFILE_FOLDER = "./profile/"
EXTENSION = ".csv"
PYTHON_FILE_BASE_NAME = "python_ai_perf"
CPP_FILE_BASE_NAME = "cpp_ai_perf"

def profile_ai_to_file(profile_name: str, game: Game, ai: GameAi):
    game.clean_players()
    game.reset_game()
    print("Starting profiling of " + profile_name)
    # Open file buffer
    with open(PROFILE_FOLDER + profile_name + EXTENSION, "a") as file:
        # Get the profiling info array
        profile_array = profile_ai(game, ai)
        # Convert to a string to be stored in the file
        profile_line = ",".join(map(str, profile_array))
        file.write(profile_line + "\n")
        # Close the file buffer
        file.close()

def profile_ai(game: Game, ai: GameAi):
    # Game loop
    performance = []
    while game.game_state() == GameState.ONGOING:
        player = game.get_player_turn()
        # prev timestamp
        time_start = time.process_time_ns()
        move = ai.getPlayerMove(player.value, game.get_game_data())
        # post timestamp
        time_end = time.process_time_ns()
        move_time = time_end - time_start
        # save movement time
        performance.append(move_time)
        # execute move to continue the game
        col = move % 3
        row = int((move - col) / 3)
        game.do_move(row, col)
    # Return the profile array when the game finishes
    return performance


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
    # Evaluates the performance of the C++ AI library compared to the Python one.
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
    python_ev_file_name = "{0}_{1}".format(PYTHON_FILE_BASE_NAME, suffix)
    cpp_ev_file_name = "{0}_{1}".format(CPP_FILE_BASE_NAME, suffix)
    for idx in range(int(test_cases)):
        # Build profile results log for Python AI
        profile_ai_to_file(python_ev_file_name, game, py_ai)
        # Build profile results log for C++ AI
        profile_ai_to_file(cpp_ev_file_name, game, cpp_ai)
    print("Performance evaluation finished. Evaluation files created:")
    print(python_ev_file_name)
    print(cpp_ev_file_name)
    graph_option()


def graph_option():
    graph_opt = ""
    while graph_opt != NO and graph_opt != YES:
        graph_opt = input("Do you want to see the evaluation results as a graph? [Y]es/[N]o: ")
        graph_opt = graph_opt.upper()
    if (graph_opt == YES):
        generate_evaluation_graph()


def generate_evaluation_graph():
    print("Generating evaluation graph...")

if __name__ == "__main__":
    evaluation()