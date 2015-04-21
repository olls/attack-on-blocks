from tkinter import *
from tkinter.ttk import *
import logging

class Gui:
    def __init__(self, master):
        self.master = master

        self.master.title("SPACE INVADERS")
        self.title = Label(master)
        self.title.config(text="SPACE INVADERS!", font=("Lucida", 30))
        self.title.pack(side="top")

        self.title2 = Button(master)
        self.title2.config(text="SPACE INVADERS!")
        self.title2.pack(side="bottom")

        # lbl_fname=Label(master)
        # lbl_fname.config(text="File Name:")
        # lbl_fname.grid(row=0, column = 0, padx=10, pady=20)

        # self.txt_fname=Entry(master)
        # self.txt_fname.grid(row=0, column=1)

        # random_button = Button(master)
        # random_button.config(text="Play File")
        # random_button.grid(row=3, column=3)

        # random_button1 = Button(master)
        # random_button1.config(text="Stop File")
        # random_button1.grid(row=3, column=2)
        logging.info("GUI Generated.")

def main():
    root=Tk()
    root.resizable(width=False, height=False)
    #root.geometry("640x480")
    front_end=Gui(root)
    root.mainloop()

if __name__ == "__main__":
    main()