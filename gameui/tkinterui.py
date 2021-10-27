from gameui.ui import Ui
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo
from ai import GameAi
from game import Game, GameState, NotEmptyTile, Player
from PIL import ImageTk, Image as PImage
import math
import threading

SQUARE_PADDING = 5
SEPARATOR_WIDTH = 2

class TkinterGui(Tk, Ui):
    def __init__(self, game: Game, ai: GameAi):
        super(TkinterGui, self).__init__()
        self.option_add('*tearOff', FALSE)
        self.title("Tic Tac Toe")
        self.minsize(500, 400)
        self.maxsize(500, 400)
        self.__game = game
        self.__ai = ai
        self.tiles = []
        self.vline_separation = 0
        self.hline_separation = 0

        mainframe = ttk.Frame(self, padding="3")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.__canvas = Canvas(mainframe, bg='white')
        self.__canvas.grid(row=0, column=0, sticky=(N, E, S, W))
    
        # Load images
        self.__x_image = PImage.open("gameui/assets/x.jpeg")
        self.__o_image = PImage.open("gameui/assets/o.jpg")
        
        self.__build_menu()
        
    def __bind_click(self):
        self.__canvas.bind('<Button-1>', self.__on_click)

    def __unbind_click(self):
        self.__canvas.unbind('<Button-1>')

    def __build_menu(self):
        menubar = Menu(self)
        menu_game = Menu(menubar)

        menu_game_options = Menu(menu_game)
        menu_game_options.add_command(label="Player vs AI", command=self.__player_vs_ai)
        menu_game_options.add_command(label="AI vs Player", command=self.__ai_vs_player)
        menu_game_options.add_command(label="Player vs Player", command=self.__player_vs_player)
        menu_game.add_cascade(label="New Game", menu=menu_game_options)

        menubar.add_cascade(menu=menu_game, label='Game')

        self.config(menu=menubar)

    def __player_vs_ai(self):
        self.__game.clean_players()
        self.__game.set_human(Player.PLAYER_1)
        self.__start_game()

    def __ai_vs_player(self):
        self.__game.clean_players()
        self.__game.set_human(Player.PLAYER_2)
        self.__start_game()

    def __player_vs_player(self):
        self.__game.clean_players()
        self.__game.set_human(Player.PLAYER_1)
        self.__game.set_human(Player.PLAYER_2)
        self.__start_game()

    def __on_game_state_change(self):
        self.__build_board(self.__canvas.winfo_width(), self.__canvas.winfo_height())
        # Check if game is finished
        game_state = self.__game.game_state()
        if not game_state == GameState.ONGOING:
            self.__endgame_actions(game_state)
            self.__unbind_click()
        elif not self.__game.is_human(self.__game.get_player_turn()):
            # AI thread
            self.ai_thread = threading.Thread(target=self.__ai_move, daemon=True)
            self.__unbind_click()
            self.ai_thread.start()
            self.__bind_click()
        else:
            self.__unbind_click()
            self.__bind_click()

    def __endgame_actions(self, game_state: GameState):
        # Stop the game
        self.stop()
        # Show end game status to the user
        message = ""
        if game_state == GameState.DRAW:
            message = "It's a DRAW!"
        if game_state == GameState.VICTORY_O:
            message = "Player O WINS!"
        if game_state == GameState.VICTORY_X:
            message = "Player X WINS!"
        showinfo("Game Over", message)
        

    def __start_game(self):
        # subscribe to game events
        self.__game.subscribe(self.__on_game_state_change)
        self.__game.reset_game()

    def __ai_move(self):
        player = self.__game.get_player_turn()
        move = self.__ai.getPlayerMove(player.value, self.__game.get_game_data())
        col = move % 3
        row = int((move - col) / 3)
        self.__game.do_move(row, col)

    def __on_click(self, event):
        player = self.__game.get_player_turn()
        if self.__game.is_human(player):
            move = self.__get_click_tile(event.x, event.y)
            try:
                self.__game.do_move(move[0], move[1])
            except NotEmptyTile:
                pass

    def __get_click_tile(self ,click_x: int, click_y: int):
        # Get x tile dimension
        if click_x < self.vline_separation:
            col = 0
        elif (self.vline_separation < click_x) and (click_x < 2 * self.vline_separation):
            col = 1
        else:
            col = 2
        # get y tile dimension
        if click_y < self.hline_separation:
            row = 0
        elif (self.hline_separation < click_y) and (click_y < 2 * self.hline_separation):
            row = 1
        else:
            row = 2
        return (row, col)    

    def __build_board(self, width: int, height: int):
        vseparation = width / 3
        hseparation = height / 3
        # vertical lines
        self.__canvas.create_line(vseparation, 0, vseparation, height, width=SEPARATOR_WIDTH)
        self.__canvas.create_line(2*vseparation, 0, 2*vseparation, height, width=SEPARATOR_WIDTH)
        # horizontal lines
        self.__canvas.create_line(0, hseparation, width, hseparation, width=SEPARATOR_WIDTH)
        self.__canvas.create_line(0, 2*hseparation, width, 2*hseparation, width=SEPARATOR_WIDTH)

        self.vline_separation = vseparation
        self.hline_separation = hseparation
        self.__draw_state(vseparation, hseparation)

    def __build_board_event(self, event: Event):
        self.__build_board(event.width, event.height)
        
    def __draw_state(self, square_width: int, square_height: int): 
        # Draw current board state
        state = self.__game.get_game_data()
        # Init tiles
        self.tiles = []
        for idx in range(len(state)):
            self.tiles.append(None)
        width = math.floor(square_width - SQUARE_PADDING)
        height =  math.floor(square_height - SQUARE_PADDING)
        for idx, tile in enumerate(state):
            if tile == Player.PLAYER_1.value:
                self.tiles[idx] = ImageTk.PhotoImage(self.__o_image.resize((width, height)))
            elif tile == Player.PLAYER_2.value:
                self.tiles[idx] = ImageTk.PhotoImage(self.__x_image.resize((width, height)))
            else:
                self.tiles[idx] = None
                continue
        for i in range(3):
            for j in range(3):
                img = self.tiles[i*3 + j]
                if tile != None:
                    posX = math.floor(j * square_width + square_width / 2)
                    posY = math.floor(i * square_height + square_height / 2)
                    self.__canvas.create_image(posX, posY, image=img)

    def start(self):
        self.mainloop()
    
    def stop(self):
        self.__unbind_click()
        self.__game.unsuscribe(self.__on_game_state_change)
        
    def update():
        pass