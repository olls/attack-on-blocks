from tkinter import *
from tkinter.ttk import *
import logging
import webbrowser
import game
from assets import Textures

PADDING_TITLE = 15
PADDING_BUTTON = 9
VERSION = {"ID":"2.2", "DATE": "19/05/15"}

class Main_Window:
    def __init__(self, master):
        self.master = master
        self.master.title("ATTACK ON BLOCKS")

        self.title = Label(self.master)
        self.title.config(text="ATTACK ON BLOCKS!",font=("Courier New", 37))
        self.title.pack(side="top", padx=PADDING_TITLE, pady=PADDING_TITLE/2)

        self.version_info = Label(self.master)
        self.version_info.config(text="Version {ID} tagged {DATE}".format(**VERSION), font=("Courier New", 13))
        self.version_info.pack(side="top", padx=0, pady=PADDING_BUTTON/2)

        self.start_button = Button(self.master, style="Menu.TButton")
        self.start_button.config(text="Play Game")
        self.start_button.pack(fill=BOTH, ipadx=PADDING_BUTTON/2, ipady=PADDING_BUTTON/2, padx=PADDING_BUTTON, pady=PADDING_BUTTON)
        self.start_button.bind('<Button-1>', self.play_game)

        self.options_button = Button(self.master, style="Menu.TButton")
        self.options_button.config(text="Show Options")
        self.options_button.pack(fill=BOTH, ipadx=PADDING_BUTTON/2, ipady=PADDING_BUTTON/2, padx=PADDING_BUTTON, pady=PADDING_BUTTON)
        self.options_button.bind('<Button-1>', self.show_options)

        self.help_button = Button(self.master, style="About.TButton")
        self.help_button.config(text="About / Help")
        self.help_button.pack(fill=BOTH, ipadx=PADDING_BUTTON/4, ipady=PADDING_BUTTON/4, padx=PADDING_BUTTON, pady=PADDING_BUTTON)
        self.help_button.bind('<Button-1>', self.show_info)

        self.exit_button = Button(self.master, style="Quit.TButton")
        self.exit_button.config(text="Quit Game")
        self.exit_button.pack(ipadx=PADDING_BUTTON/3, ipady=PADDING_BUTTON, padx=PADDING_BUTTON, pady=PADDING_BUTTON)
        self.exit_button.bind('<Button-1>', self.close)

        self.about_info = Label(self.master)
        self.about_info.config(text="Game Created by TheOrangeOne!", font=("Courier New", 9))
        self.about_info.bind("<Button-1>", self.show_site)
        self.about_info.pack(side="top", padx=0, pady=PADDING_BUTTON/2)

        Style().configure("Menu.TButton", font=("Lucida", 21))
        Style().configure("About.TButton", font=("Lucida", 17))
        Style().configure("Quit.TButton", font=("Lucida", 13))

        self.options_window = Options_Window()
        logging.debug("GUI Generated.")

    def play_game(self, event):
        self.master.withdraw()
        exit_code = game.initialise(self.master, self.options_window.options)
        if exit_code != "QUIT": self.title["text"] = exit_messages[exit_code]

    def show_options(self, event):
        self.new_window = Toplevel(self.master)
        self.options_window.display(self.new_window)

    def show_info(self, event):
        logging.info("Loading About Page...")
        webbrowser.open("https://bitbucket.org/theorangeone/attack-on-blocks/wiki/Home")

    def close(self, event):
        logging.critical("Closing Main Window.")
        self.master.destroy()

    def show_site(self, event):
        logging.info("Loading Website")
        webbrowser.open("http://theorangeone.net")

class Options_Window:
    def __init__(self):
        self.textures_object = Textures()
        self.options = {
            "Difficulty": 120,
            "Textures": self.textures_object,
            "Sounds": True
        }

    def display(self, master):
        self.master = master
        self.master.title("ATTACK ON BLOCKS - Options")

        self.title = Label(self.master)
        self.title.config(text="OPTIONS",font=("Courier New", 37))
        self.title.pack(side="top", padx=PADDING_TITLE, pady=PADDING_TITLE/2)

        self.difficulty_title = Label(self.master)
        self.difficulty_title.config(text="Current Difficulty: {}".format(self.options["Difficulty"]), font=("Courier New", 13))
        self.difficulty_title.pack(ipadx=PADDING_BUTTON/3, padx=PADDING_BUTTON)
        self.difficulty_scale = Scale(self.master, from_=5, to=500, orient="horizontal", command=self.update_difficulty, length=350)
        self.difficulty_scale.pack(ipadx=PADDING_BUTTON/3, padx=PADDING_BUTTON/3)
        self.difficulty_scale["value"] = self.options["Difficulty"]
        self.difficulty_reset_button = Button(self.master, style="Minor.TButton")
        self.difficulty_reset_button.config(text="Reset Difficulty")
        self.difficulty_reset_button.pack(ipadx=PADDING_BUTTON/3, padx=PADDING_BUTTON/3)
        self.difficulty_reset_button.bind('<Button-1>', self.reset_difficulty)

        Frame(self.master,height=23).pack()

        self.texture_title = Label(self.master)
        self.texture_title.config(text="Select Texture Pack", font=("Courier New", 13))
        self.texture_title.pack(ipadx=PADDING_BUTTON/3, padx=PADDING_BUTTON)
        self.texture_select = Listbox(master)
        self.texture_select.delete(0, END)
        for directory in self.options["Textures"].list_packs():
            if directory == "": continue
            self.texture_select.insert(END, directory)
        self.texture_select.pack(ipadx=PADDING_BUTTON/3, padx=PADDING_BUTTON/3)

        Frame(self.master,height=23).pack()

        self.using_sounds = IntVar()
        self.using_sounds.set(self.options["Sounds"])
        self.sounds_check = Checkbutton(self.master, text="Use Sound Effects", command=self.update_sounds, variable=self.using_sounds)
        self.sounds_check.pack(ipadx=PADDING_BUTTON/3, padx=PADDING_BUTTON)

        Style().configure("Minor.TButton", font=("Lucida", 10))
        self.master.protocol('WM_DELETE_WINDOW', self.close)
        logging.info("Options menu created.")

    def close(self):
        self.options["Textures"].pack = self.texture_select.get(ACTIVE) if self.texture_select.get(ACTIVE) != "" else "default" # Because it has no changed event
        logging.info("Selected Texture Pack: {}".format(self.options["Textures"].pack))
        self.master.destroy()

    def update_sounds(self):
        self.options["Sounds"] = self.using_sounds.get()

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