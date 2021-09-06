from ai import GameAi
from game import Game, GameState, NotEmptyTile, Player

class Ui:
    def start(self):
        pass
    def stop(self):
        pass
    def update(self):
        pass

class ConsoleUi(Ui):
    def __init__(self, game: Game, ai: GameAi):
        self.__game = game
        self.__ai = ai

    def __del__(self):
        self.stop()

    def __ui_loop(self):
        self.__game.set_human(Player.PLAYER_1)
        while self.__game.game_state() == GameState.ONGOING:
            player = self.__game.get_player_turn()
            if self.__game.is_human(player):
                move = input('Enter your move {} (<row> <col>):\n'.format(player.value))
                if move == 'q':
                    break
                moveList = move.split(' ')
                if len(moveList) != 2:
                    print('You should enter two values for row and col.')
                else:
                    try:
                        moveList = list(map(lambda idx : int(idx), moveList))
                        self.__game.do_move(moveList[0], moveList[1])
                    except ValueError:
                        print('<row> and <col> values must be integers between 0 and 2')
                    except NotEmptyTile:
                        print('Move already done before')
            else:
                print('{} turn (AI):\n'.format(player.value))
                move = self.__ai.getPlayerMove(player.value, self.__game.get_game_data())
                col = move % 3
                row = int((move - col) / 3)
                self.__game.do_move(row, col)
        self.__end_game_message(self.__game.game_state())
        

    def __end_game_message(self, state: GameState):
        print('End game: ')
        if state == GameState.DRAW:
            print('DRAW\n')
        if state == GameState.VICTORY_O:
            print('PlAYER {0} WINS!\n'.format(Player.PLAYER_1.value))
        if state == GameState.VICTORY_X:
            print('PLAYER {0} WINS!\n'.format(Player.PLAYER_2.value))

    def start(self):
        self._callback = self.update
        self.__game.subscribe(self._callback)
        self.__ui_loop()

    def stop(self):
        self.__game.unsuscribe(self._callback)

    def update(self):
        line = "| "
        game_data = self.__game.get_game_data()
        for idx, value in enumerate(game_data):
            line = line + str(value) + " "
            if (idx + 1) % 3 == 0:
                line = line + "|"
                print(line)
                line = "| "
        print('\n\n')
