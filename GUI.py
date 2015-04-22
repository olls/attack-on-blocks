from tkinter import *
from tkinter.ttk import *
import logging
import game
PADDING_TITLE = 15
PADDING_BUTTON = 9

PROGRAM_OPEN = True

class Main_Window:
    def __init__(self, master):
        self.master = master
        self.master.title("SPACE INVADERS")

        self.title = Label(self.master)
        self.title.config(text="SPACE INVADERS!",font=("Courier New", 37))
        self.title.pack(side="top", padx=PADDING_BUTTON, pady=PADDING_TITLE/2)

        self.start_button = Button(self.master, style="Menu.TButton")
        self.start_button.config(text="Play Game")
        self.start_button.pack(fill=BOTH, ipadx=PADDING_BUTTON/2, ipady=PADDING_BUTTON/2, padx=PADDING_BUTTON, pady=PADDING_BUTTON)
        self.start_button.bind('<Button-1>', self.play_game)

        self.exit_button = Button(self.master, style="Quit.TButton")
        self.exit_button.config(text="Quit Game")
        self.exit_button.pack(ipadx=PADDING_BUTTON/3, ipady=PADDING_BUTTON, padx=PADDING_BUTTON, pady=PADDING_BUTTON)
        self.exit_button.bind('<Button-1>', self.close)


        Style().configure("Menu.TButton", font=("Lucida", 25 ))
        Style().configure("Quit.TButton", font=("Lucida", 15))

        logging.info("GUI Generated.")

    def play_game(self, event):
        logging.info("Game Started.")
        self.master.withdraw()
        game.initialise(self.master, None)

    def close(self, event):
        logging.critical("Closing Main Window.")
        self.master.destroy()



def display():
    root=Tk()
    root.resizable(width=False, height=False)
    front_end=Main_Window(root)
    root.mainloop()


logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)


if __name__ == "__main__":
    display()