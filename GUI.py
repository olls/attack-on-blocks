from tkinter import *
from tkinter.ttk import *
import logging
import game


PADDING_TITLE = 15
PADDING_BUTTON = 9


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

        self.start_button = Button(self.master, style="Menu.TButton")
        self.start_button.config(text="Show Options")
        self.start_button.pack(fill=BOTH, ipadx=PADDING_BUTTON/2, ipady=PADDING_BUTTON/2, padx=PADDING_BUTTON, pady=PADDING_BUTTON)
        self.start_button.bind('<Button-1>', self.show_options)

        self.exit_button = Button(self.master, style="Quit.TButton")
        self.exit_button.config(text="Quit Game")
        self.exit_button.pack(ipadx=PADDING_BUTTON/3, ipady=PADDING_BUTTON, padx=PADDING_BUTTON, pady=PADDING_BUTTON)
        self.exit_button.bind('<Button-1>', self.close)

        Style().configure("Menu.TButton", font=("Lucida", 25))
        Style().configure("Quit.TButton", font=("Lucida", 15))

        self.options_window = Options_Window()
        logging.debug("GUI Generated.")

    def play_game(self, event):
        self.master.withdraw()
        exit_code = game.initialise(self.master, self.options_window.options)
        if exit_code != "QUIT": self.title["text"] = exit_messages[exit_code]

    def show_options(self, event):
        self.new_window = Toplevel(self.master)
        self.options_window.display(self.new_window)

    def close(self, event):
        logging.critical("Closing Main Window.")
        self.master.destroy()


class Options_Window:
    def __init__(self):
    	self.textures = Textures()
        self.options = {
            "Difficulty": 120,
            "Textures": self.textures
        }

    def display(self, master):
        self.master = master
        self.master.title("SPACE INVADERS - Options")

        self.title = Label(self.master)
        self.title.config(text="OPTIONS",font=("Courier New", 37))
        self.title.pack(side="top", padx=PADDING_TITLE, pady=PADDING_TITLE/2)

        self.difficulty_title = Label(self.master)
        self.difficulty_title.config(text="Current Difficulty: {}".format(self.options["Difficulty"]), font=("Courier New", 19))
        self.difficulty_title.pack(ipadx=PADDING_BUTTON/3, padx=PADDING_BUTTON)

        self.difficulty_scale = Scale(self.master, from_=30, to=300, orient="horizontal", command=self.update_difficulty, length=400)
        self.difficulty_scale.pack(ipadx=PADDING_BUTTON/3, padx=PADDING_BUTTON/3)

        self.exit_button = Button(self.master, style="Minor.TButton")
        self.exit_button.config(text="Reset")
        self.exit_button.pack(ipadx=PADDING_BUTTON/3, padx=PADDING_BUTTON/3)
        self.exit_button.bind('<Button-1>', self.reset_difficulty)

        Style().configure("Minor.TButton", font=("Lucida", 10))
        logging.info("Options menu created.")
        
    def close(self):
        self.master.destroy()

    def update_difficulty(self, event):
        self.options["Difficulty"] = int(self.difficulty_scale.get())
        self.difficulty_title["text"] = "Current Difficulty: {}".format(self.options["Difficulty"])

    def reset_difficulty(self, event):
        self.options["Difficulty"] = 120
        self.difficulty_title["text"] = "Current Difficulty: {}".format(self.options["Difficulty"])
        self.difficulty_scale["value"] = 120


def display():
    root=Tk()
    root.resizable(width=False, height=False)
    front_end=Main_Window(root)
    root.mainloop()


exit_messages = {
    "LIVES":"You ran out of lives!",
    "PLAYER COLLISION":"The enemies got to you!"
}

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)


if __name__ == "__main__":
    display()