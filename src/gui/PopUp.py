from tkinter import *
from src.gui.BoardGUI import BoardGUI
from tkinter import messagebox
from PIL import ImageTk, Image
import os.path

def show_popup(prev_main,mode):
    level=IntVar(value=2)
    algo=IntVar(value=1)



    def handle_selection():
        selected_option_level = level.get()
        selected_option_algo = algo.get()
        print(selected_option_level,selected_option_algo)
        main.withdraw()
        prev_main.withdraw()
        if mode== "AI_ANY":
            messagebox.showinfo(title="For Rana", message="Put ur implement here")
        else:
            BoardGUI(mode,selected_option_level,selected_option_algo)

    def handle_choice_level(value):
        level.set(value)

    def handle_choice_algo(value):
        algo.set(value)

    main = Tk()
    main.config(width=300, height=175)
    my_canvas = Canvas(main, width=300, height=175)
    my_canvas.pack(fill="both", expand=True)

    # Title
    main.title("Ai Agent Settings")

    #Level
    label = Label(main, text="Select Ai Agent Level")
    my_canvas.create_window(150, 20, window=label)

    option1 = Radiobutton(main, text="Easy",variable=level, value=2,command=lambda:handle_choice_level(2))
    option1.select()
    my_canvas.create_window(50, 50, window=option1)

    option2 = Radiobutton(main, text="Medium",variable=level, value=4,command=lambda:handle_choice_level(4))
    my_canvas.create_window(150, 50, window=option2)

    option3 = Radiobutton(main, text="Hard",variable=level, value=6,command=lambda:handle_choice_level(6))
    my_canvas.create_window(250, 50, window=option3)

    #Algo
    labelAlgo = Label(my_canvas, text="Select Ai Agent Algorithm")
    my_canvas.create_window(150, 80, window=labelAlgo)

    option1Algo = Radiobutton(my_canvas, text="Alpha-Beta",variable=algo, value=1,command=lambda:handle_choice_algo(1))
    option1Algo.select()
    my_canvas.create_window(100, 110, window=option1Algo)

    option2Algo = Radiobutton(my_canvas, text="Min-Max",variable=algo, value=2,command=lambda:handle_choice_algo(2))
    my_canvas.create_window(200, 110, window=option2Algo)

    submit_button = Button(my_canvas, text="Submit", command=handle_selection)
    my_canvas.create_window(150, 150, window=submit_button)

    main.mainloop()

