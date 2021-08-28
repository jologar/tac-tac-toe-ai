from gameui.ui import Ui
from tkinter import *
from tkinter import ttk
from ai import GameAi
from game import Game

class TkinterGui(Tk, Ui):
    def __init__(self, game: Game, ai: GameAi):
        super(TkinterGui, self).__init__()
        self.option_add('*tearOff', FALSE)
        self.title("Tic Tac Toe")
        self.minsize(500, 400)
        self.maxsize(500, 400)

        mainframe = ttk.Frame(self, padding="3")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.__canvas = Canvas(mainframe, bg='white')
        self.__canvas.bind("<Configure>", self.__build_board)
        self.__canvas.grid(row=0, column=0, sticky=(N, E, S, W))
        
        self.__buildMenu()
        
    
    def __buildMenu(self):
        menubar = Menu(self)
        menu_game = Menu(menubar)
        menubar.add_cascade(menu=menu_game, label='Game')
        menu_game.add_command(label="New Game", command=self.__start_new_game)
        # TODO: build the menu
        
        self.config(menu=menubar)
    
    def __start_new_game(self):
        print('Start new game!')

    def __build_board(self, event: Event):
        vseparation = event.width / 3
        hseparation = event.height / 3
        # vertical lines
        self.__canvas.create_line(vseparation, 0, vseparation, event.height, width=4)
        self.__canvas.create_line(2*vseparation, 0, 2*vseparation, event.height, width=4)
        # horizontal lines
        self.__canvas.create_line(0, hseparation, event.width, hseparation, width=4)
        self.__canvas.create_line(0, 2*hseparation, event.width, 2*hseparation, width=4)


    def start(self):
        self.mainloop()
    
    def stop():
        pass
    def update():
        pass