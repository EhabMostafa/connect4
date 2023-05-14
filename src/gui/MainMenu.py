import tkinter
from tkinter import *
from PIL import ImageTk, Image
import os.path
from src.gui.BoardGUI import BoardGUI

class MainMenu:
    mode="Human_Human"

    def __init__(self):
        main = Tk()
        main.config(width=800,height=800)

        #Title
        main.title("Connect4")

        #BackGround
        script_dir = os.path.dirname(os.path.abspath(__file__))
        bg = ImageTk.PhotoImage(Image.open(os.path.join(script_dir, '../assets/connect4Back.png')))
        my_canvas = Canvas(main,width=800,height=800)
        my_canvas.pack(fill="both",expand=True)
        my_canvas.create_image(0,0,image=bg,anchor="nw")


        # Human Vs Human Button
        humanHumanButton = Button(main, text="Human VS Human", width=25,command=lambda: self.selectMode("Human_Human",main))
        my_canvas.create_window(400, 400, window=humanHumanButton)

        # Human Vs AI Button
        humanAIButton = Button(main, text="Human VS AI", width=25,command=lambda:self.selectMode("Human_AI",main))
        my_canvas.create_window(400, 450, window=humanAIButton)

        # Computer VS AI Button
        computerAIButton = Button(main, text="Computer VS AI", width=25,command=lambda:self.selectMode("Computer_AI",main))
        my_canvas.create_window(400, 500, window=computerAIButton)

        # Exit Button
        exitButton = Button(main, text="Exit", width=25,command=main.destroy)
        my_canvas.create_window(400, 750, window=exitButton)


        main.mainloop()



    def selectMode(self,newMode,main):
        mode=newMode
        main.withdraw()
        BoardGUI(mode)


