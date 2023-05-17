import numpy as np
import random
import math


class AIAgent:
    def winning_move(board, piece,width,heigth):
        # Check horizontal locations for win
        for c in range(heigth - 3):
            for r in range(width):
                if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                    c + 3] == piece:
                    return True

        # Check vertical locations for win
        for c in range(heigth):
            for r in range(width - 3):
                if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                    c] == piece:
                    return True

        # Check positively sloped diaganols
        for c in range(heigth - 3):
            for r in range(width - 3):
                if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and \
                        board[r + 3][c + 3] == piece:
                    return True

        # Check negatively sloped diaganols
        for c in range(heigth - 3):
            for r in range(3, width):
                if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and \
                        board[r - 3][c + 3] == piece:
                    return True

    def get_position_score(board, piece,width,heigth):
        score = 0

        ## Score center column
        center_array = [int(i) for i in list(board[:, heigth // 2])]
        center_count = center_array.count(piece)
        score += center_count * 3

        ## Score Horizontal
        for r in range(width):
            row_array = [int(i) for i in list(board[r, :])]
            for c in range(heigth - 3):
                window = row_array[c:c + 4]
                score += AIAgent.EvaluateWindow(window, piece)

        ## Score Vertical
        for c in range(heigth):
            col_array = [int(i) for i in list(board[:, c])]
            for r in range(width - 3):
                window = col_array[r:r + 4]
                score += AIAgent.EvaluateWindow(window, piece)

        ## Score posiive sloped diagonal
        for r in range(width - 3):
            for c in range(heigth - 3):
                window = [board[r + i][c + i] for i in range(4)]
                score += AIAgent.EvaluateWindow(window, piece)

        for r in range(width - 3):
            for c in range(heigth - 3):
                window = [board[r + 3 - i][c + i] for i in range(4)]
                score += AIAgent.EvaluateWindow(window, piece)

        return score

    def put_piece(board, Row, colum, piece):
        board[Row][colum] = piece

    def Stop(board,width,heigth):
        return AIAgent.winning_move(board, 1,width,heigth) or AIAgent.winning_move(board, 2,width,heigth) or len(
            AIAgent.avaiableLocations(board,width,heigth)) == 0

    def avaiableLocation(board, colum,width):
        return board[width - 1][colum] == 0

    def avaiableLocations(board,width,heigth):
        valid_locations = []
        for c in range(heigth):
            if AIAgent.avaiableLocation(board, c,width):
                valid_locations.append(c)
        return valid_locations

    def avaiableRow(board, colum,width):
        for row in range(width):
            if board[row][colum] == 0:
                return row

    def EvaluateWindow(window, piece):
        score = 0
        opponent_piece = 1
        if piece == 1:
            opponent_piece = 2

        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(0) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(0) == 2:
            score += 2

        if window.count(opponent_piece) == 3 and window.count(0) == 1:
            score -= 4

        return score
    def Alpha_Beta_Pruning(board, width, heigth, depth, alpha, beta, MaxPlayer):

        board = np.array(board)
        valid_locations = AIAgent.avaiableLocations(board,width,heigth)
        is_terminal = AIAgent.Stop(board,width,heigth)
        if depth == 0 or is_terminal:
            if is_terminal:
                if AIAgent.winning_move(board, 2,width,heigth):
                    return (None, 100000000000000)
                elif AIAgent.winning_move(board, 1,width,heigth):
                    return (None, -10000000000000)
                else:  # Game is over, no more valid moves
                    return (None, 0)
            else:  # Depth is zero
                return (None, AIAgent.get_position_score(board, 2,width,heigth))
        if MaxPlayer:
            value = -math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = AIAgent.avaiableRow(board, col,width)
                copyBoard = board.copy()
                AIAgent.put_piece(copyBoard, row, col, 2)
                new_score = AIAgent.Alpha_Beta_Pruning(copyBoard, width, heigth, depth - 1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value

        else:  # Minimizing player
            value = math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = AIAgent.avaiableRow(board, col,width)
                copyBoard = board.copy()
                AIAgent.put_piece(copyBoard, row, col, 1)
                new_score = AIAgent.Alpha_Beta_Pruning(copyBoard, width, heigth, depth - 1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value

    def minmax(board, width, heigth, depth, maximizing_player):
        valid_locations = AIAgent.avaiableLocations(board, width, heigth)
        is_terminal = AIAgent.Stop(board, width, heigth)

        if depth == 0 or is_terminal:
            if is_terminal:
                if AIAgent.winning_move(board, 2,width,heigth):
                    return (None, 100000000000000)  # Positive infinity
                elif AIAgent.winning_move(board, 1,width,heigth):
                    return (None, -10000000000000)  # Negative infinity
                else:  # Game is over, no more valid moves
                    return (None, 0)
            else:  # Depth is zero
                return (None, AIAgent.get_position_score(board,2,width,heigth))

        if maximizing_player:
            value = -math.inf  # Negative infinity
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = AIAgent.avaiableRow(board,col,width)
                copyBoard = board.copy()
                AIAgent.put_piece(copyBoard,row,col,2)
                new_score = AIAgent.minmax(copyBoard,width,heigth, depth - 1, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
            return column, value
        else:  # Minimizing player
            value = math.inf  # Positive infinity
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = AIAgent.avaiableRow(board,col,width)
                copyBoard = board.copy()
                AIAgent.put_piece(copyBoard,row,col,1)
                new_score = AIAgent.minmax(copyBoard,width,heigth, depth - 1, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
            return column, value

    def Minimax(board, width, height, depth, maximizing_player):
        board = np.array(board)
        return AIAgent.minmax(board,width, height,depth, maximizing_player)
