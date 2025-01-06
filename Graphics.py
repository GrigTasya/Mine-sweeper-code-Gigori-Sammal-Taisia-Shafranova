#minesweeper graphics
import pygame

BOMB = "B"
FLAG = ">"
MIS_FLAG = "<"

RED = (255, 0, 0)
BLACK = (0,0,0)
LOST_CASE = (134, 62, 7)

def DrawSquare(size, x, y, SquareBackground, SquareBoarders, Window):
    
    pygame.draw.rect(Window, SquareBackground, pygame.Rect(x, y, size, size))
    pygame.draw.rect(Window, SquareBoarders, pygame.Rect(x, y, size, size), 4)
    #corpse = pygame.image.load("Burned_man.png").convert_alpha()


def Draw_cell(FieldClean, FieldOpen, CurrentRow, CurrentColl, SquareX, SquareY, NumberColour, SquareSize, SquaresBackgroundColour, SquaresBoardersColour, Window):
    DrawSquare(SquareSize, SquareX, SquareY, SquaresBackgroundColour, SquaresBoardersColour, Window)
    
    if FieldClean[CurrentRow][CurrentColl] == ".":
        # The cell is closed
        pass
    else:
        # The cell is openned
        FontSize = int(SquareSize * 0.8)
        NumberX = SquareX + (SquareSize / 2) - (FontSize / 6)
        NumberY = SquareY + (SquareSize / 2) - (FontSize / 4.5)

        if FieldClean[CurrentRow][CurrentColl] == FLAG:
            Draw_on_a_cell(FLAG, NumberX, NumberY, NumberColour, FontSize, Window)

        elif FieldClean[CurrentRow][CurrentColl] == "-":
            Draw_empty_cell(SquareSize, SquareX, SquareY, Window)

        elif FieldClean[CurrentRow][CurrentColl] == MIS_FLAG:
            DrawSquare(SquareSize, SquareX, SquareY, LOST_CASE, LOST_CASE, Window)
            Draw_on_a_cell(FLAG, NumberX, NumberY, NumberColour, FontSize, Window)

        elif FieldOpen[CurrentRow][CurrentColl] != BOMB:
            Num = FieldClean[CurrentRow][CurrentColl]
            Draw_on_a_cell(Num, NumberX, NumberY, NumberColour, FontSize, Window)

        elif FieldOpen[CurrentRow][CurrentColl] == BOMB:
            Num = FieldClean[CurrentRow][CurrentColl]
            Draw_on_a_cell(Num, NumberX, NumberY, NumberColour, FontSize, Window)


def Draw_on_a_cell(Something, x, y, NumberColour, font_size, screen):
    font = pygame.font.Font(None, font_size)
    text = font.render(Something, True, NumberColour)
    screen.blit(text, (x, y))


def Draw_empty_cell(size, x, y, Window):
    EmptyCellColour = (139,82,8)
    pygame.draw.rect(Window, EmptyCellColour, pygame.Rect(x, y, size, size))


def Draw_the_board(FieldClean, FieldOpen, ScreenWidth, StartX, StartY, NumberColour, SquaresBackgroundColour, SquaresBoardersColour, Window):
    Rows = len(FieldOpen)
    Cols = len(FieldOpen[0])
    SquareSize = ScreenWidth // Cols

    for i in range(Rows):
        for j in range(Cols):
            X_for_square = StartX + j * SquareSize
            Y_for_square = StartY + i * SquareSize

            Draw_cell(FieldClean, FieldOpen, i, j, X_for_square, Y_for_square, NumberColour, SquareSize, SquaresBackgroundColour, SquaresBoardersColour, Window)



def Draw_ChangeDifficulty(Difficulty, Colour, width, height, x, y, colour, Window):
    corner_radius = 20
    pygame.draw.rect(Window, colour, (x, y, width, height), border_radius=corner_radius)
    Font_for_DifficultyChange =  pygame.font.Font(None, 23)
    ChangeDifficulty = Font_for_DifficultyChange.render(f"{Difficulty}", True, Colour)
    Window.blit(ChangeDifficulty, (40,20))

    

def BombCounter(BombCounter, Colour, Window):
    Font_for_Bomb = pygame.font.Font(None, 36)
    Bombs = Font_for_Bomb.render(f"{BombCounter:3d}", True, Colour)
    Window.blit(Bombs, (150, 5))
