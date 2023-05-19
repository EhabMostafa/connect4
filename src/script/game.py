from src.script.board import Board
import time
import random
import math

from src.classes.AIAgent import AIAgent
import webbrowser

# GAME LINK
# http://kevinshannon.com/connect4/


def ai_script(mode,level,algo):
    board_Width = 6  # Mean number of rows
    board_Height = 7  # Mean number of Cols

    board = Board()

    webbrowser.open('http://kevinshannon.com/connect4/')

    time.sleep(5)
    game_end = False

    while not game_end:
        (game_board, game_end) = board.get_game_grid()

        # FOR DEBUG PURPOSES
        board.print_grid(game_board)
        print("\n")

        # YOUR CODE GOES HERE

        # Insert here the action you want to perform based on the output of the algorithm
        # You can use the following function to select a column
        #random_column = random.randint(0, 6)


        board_for_agent= list(reversed(board.board))

        if algo == 1:
            col, _ = AIAgent.Alpha_Beta_Pruning(board_for_agent, board_Width, board_Height, level,-math.inf, math.inf, True)
        else:
            col, _ = AIAgent.Minimax(board_for_agent, board_Width, board_Height, level, True)

        board.select_column(col)

        time.sleep(2)



