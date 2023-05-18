import time

import pygame
import sys
import math
import random
from src.classes.AIAgent import AIAgent


BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


class BoardGUI:

    board_Width = 6
    board_Height = 7
    square_size = 100
    board = []
    turn = 1
    game_end = False
    player1 = "H1"
    player2 = "H2"
    mode = "Human_Human"
    level = "easy"

    def makeBoard(self):
        self.board = []
        for i in range(self.board_Width):
            row = []
            for j in range(self.board_Height):
                row.append(0)
            self.board.append(row)

    def selectMode(self, mode):
        self.mode = mode

        if self.mode == "Human_Human":
            self.player1 = "H1"
            self.player2 = "H2"

        elif self.mode == "Human_AI":
            self.player1 = "HU"
            self.player2 = "AI"

        elif self.mode == "Computer_AI":
            self.player1 = "COM"
            self.player2 = "AI"

    def drop_piece(self, board, row, col, piece):
        board[row][col] = piece

    def is_valid_location(self, board, col):
        return board[self.board_Width - 1][col] == 0

    def get_next_open_row(self, board, col):
        for r in range(self.board_Width):
            if board[r][col] == 0:
                return r

    def draw_board(self, board, screen, radius, height, myfont):

        for c in range(self.board_Height):
            for r in range(self.board_Width):
                pygame.draw.rect(screen, YELLOW, (c * self.square_size, r *
                                 self.square_size + self.square_size, self.square_size, self.square_size))
                pygame.draw.circle(screen, WHITE, (
                    int(c * self.square_size + self.square_size / 2), int(r * self.square_size + self.square_size + self.square_size / 2)), radius)

        for c in range(self.board_Height):
            for r in range(self.board_Width):
                if board[r][c] == 1:
                    pygame.draw.circle(screen, RED, (
                        int(c * self.square_size + self.square_size / 2), height - int(r * self.square_size + self.square_size / 2)), radius)

                    label = myfont.render(self.player1, 1, WHITE)
                    screen.blit(label, label.get_rect(center=(int(
                        c * self.square_size + self.square_size / 2), height - int(r * self.square_size + self.square_size / 2))))

                elif board[r][c] == 2:
                    pygame.draw.circle(screen, BLUE, (
                        int(c * self.square_size + self.square_size / 2), height - int(r * self.square_size + self.square_size / 2)), radius)

                    label = myfont.render(self.player2, 1, WHITE)
                    screen.blit(label, label.get_rect(center=(int(
                        c * self.square_size + self.square_size / 2), height - int(r * self.square_size + self.square_size / 2))))

        pygame.display.update()

    def winning_move(self, board, piece):
        # Check horizontal locations for win
        for c in range(self.board_Height - 3):
            for r in range(self.board_Width):
                if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                        c + 3] == piece:
                    return True

        # Check vertical locations for win
        for c in range(self.board_Height):
            for r in range(self.board_Width - 3):
                if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                        c] == piece:
                    return True

        # Check positively sloped diaganols
        for c in range(self.board_Height - 3):
            for r in range(self.board_Width - 3):
                if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and \
                        board[r + 3][c + 3] == piece:
                    return True

        # Check negatively sloped diaganols
        for c in range(self.board_Height - 3):
            for r in range(3, self.board_Width):
                if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and \
                        board[r - 3][c + 3] == piece:
                    return True

    def __init__(self, mode):

        self.makeBoard()
        self.selectMode(mode)

        # Lets implement GUI
        pygame.init()

        width = self.board_Height * self.square_size
        height = (self.board_Width + 1) * self.square_size
        size = (width, height)
        radius = int(self.square_size / 2 - 5)

        screen = pygame.display.set_mode(size)
        screen.fill(WHITE)

        myfont = pygame.font.SysFont("monospace", 72)
        myfontPiece = pygame.font.SysFont("monospace", 40)

        self.draw_board(self.board, screen, radius, height, myfontPiece)

        # will add here modes

        while not self.game_end:

            if self.mode == "Human_Human":

                for event in pygame.event.get():

                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.MOUSEMOTION:
                        pygame.draw.rect(
                            screen, WHITE, (0, 0, width, self.square_size))
                        posx = event.pos[0]
                        if self.turn == 1:
                            pygame.draw.circle(
                                screen, RED, (posx, int(self.square_size / 2)), radius)
                            label = myfontPiece.render(self.player1, 1, WHITE)
                            screen.blit(label, label.get_rect(
                                center=(posx, int(self.square_size / 2))))
                        else:
                            pygame.draw.circle(
                                screen, BLUE, (posx, int(self.square_size / 2)), radius)
                            label = myfontPiece.render(self.player2, 1, WHITE)
                            screen.blit(label, label.get_rect(
                                center=(posx, int(self.square_size / 2))))
                    pygame.display.update()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pygame.draw.rect(
                            screen, WHITE, (0, 0, width, self.square_size))
                        # print(event.pos)
                        # Ask for Player 1 Input
                        if self.turn == 1:
                            posx = event.pos[0]
                            col = int(math.floor(posx / self.square_size))

                            if self.is_valid_location(self.board, col):
                                row = self.get_next_open_row(self.board, col)
                                self.drop_piece(self.board, row, col, 1)

                                if self.winning_move(self.board, 1):
                                    label = myfont.render(
                                        "Player 1 wins!!", 1, RED)
                                    screen.blit(label, (40, 10))
                                    self.game_end = True

                        # # Ask for Player 2 Input
                        else:
                            posx = event.pos[0]
                            col = int(math.floor(posx / self.square_size))

                            if self.is_valid_location(self.board, col):
                                row = self.get_next_open_row(self.board, col)
                                self.drop_piece(self.board, row, col, 2)

                                if self.winning_move(self.board, 2):
                                    label = myfont.render(
                                        "Player 2 wins!!", 1, BLUE)
                                    screen.blit(label, (40, 10))
                                    self.game_end = True

                        self.draw_board(self.board, screen,
                                        radius, height, myfontPiece)

                        if self.turn == 1:
                            self.turn = 2
                        else:
                            self.turn = 1

            elif self.mode == 'Human_AI':
                for event in pygame.event.get():

                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.MOUSEMOTION:
                        pygame.draw.rect(
                            screen, WHITE, (0, 0, width, self.square_size))
                        posx = event.pos[0]
                        if self.turn == 1:
                            pygame.draw.circle(
                                screen, RED, (posx, int(self.square_size / 2)), radius)
                            label = myfontPiece.render(self.player1, 1, WHITE)
                            screen.blit(label, label.get_rect(
                                center=(posx, int(self.square_size / 2))))

                    pygame.display.update()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # Ask for Player 1 Input
                        if self.turn == 1:
                            pygame.draw.rect(
                                screen, WHITE, (0, 0, width, self.square_size))
                            posx = event.pos[0]
                            col = int(math.floor(posx / self.square_size))

                            if self.is_valid_location(self.board, col):
                                row = self.get_next_open_row(self.board, col)
                                self.drop_piece(self.board, row, col, 1)

                                if self.winning_move(self.board, 1):
                                    label = myfont.render(
                                        "Player 1 wins!!", 1, RED)
                                    screen.blit(label, (40, 10))
                                    self.game_end = True
                        self.draw_board(self.board, screen,
                                        radius, height, myfontPiece)

                        # # Ask for Player 2 Input

                        # 2for easy,4for medium,6 for hard
                        col, _ = AIAgent.Alpha_Beta_Pruning(
                            self.board, self.board_Width, self.board_Height, 6, -math.inf, math.inf, True)
                        # col, _ = AIAgent.Minimax(self.board, self.board_Width, self.board_Height, 6, True)#2for easy,4for medium,6 for hard
                        if self.is_valid_location(self.board, col):
                            row = self.get_next_open_row(self.board, col)
                            self.drop_piece(self.board, row, col, 2)

                            if self.winning_move(self.board, 2):
                                label = myfont.render(
                                    "Player 2 wins!!", 1, BLUE)
                                screen.blit(label, (40, 10))
                                self.game_end = True

                        self.draw_board(self.board, screen,
                                        radius, height, myfontPiece)

                        if self.turn == 1:
                            self.turn = 2
                        else:
                            self.turn = 1

            elif self.mode == "Computer_AI":

                if self.turn == 1:
                    col = random.randint(0, self.board_Height-1)

                    if self.is_valid_location(self.board, col):
                        row = self.get_next_open_row(self.board, col)
                        self.drop_piece(self.board, row, col, 1)

                        if self.winning_move(self.board, 1):
                            label = myfont.render("Player 1 wins!!", 1, RED)
                            screen.blit(label, (40, 10))
                            self.game_end = True
                else:
                    # 2for easy,4for medium,6 for hard
                    col, _ = AIAgent.Alpha_Beta_Pruning(
                        self.board, self.board_Width, self.board_Height, 6, -math.inf, math.inf, True)
                    # col, _ = AIAgent.Minimax(self.board, self.board_Width, self.board_Height, 6, True)#2for easy,4for medium,6 for hard
                    if self.is_valid_location(self.board, col):
                        row = self.get_next_open_row(self.board, col)
                        self.drop_piece(self.board, row, col, 2)

                        if self.winning_move(self.board, 2):
                            label = myfont.render("Player 2 wins!!", 1, BLUE)
                            screen.blit(label, (40, 10))
                            self.game_end = True

                self.draw_board(self.board, screen, radius,
                                height, myfontPiece)

                if self.turn == 1:
                    self.turn = 2
                else:
                    self.turn = 1

                time.sleep(1)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
