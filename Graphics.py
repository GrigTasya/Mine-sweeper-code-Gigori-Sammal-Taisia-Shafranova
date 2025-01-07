#minesweeper graphics
import pygame

BOMB = "B"
FLAG = ">"
MIS_FLAG = "<"

RED = (255, 0, 0)
BLACK = (0,0,0)
LOST_CASE = (134, 62, 7)

# THE NUMBERS
Num1 = pygame.image.load("Textures\\Number 1.png")
Num2 = pygame.image.load("Textures\\Number 2.png")
Num3 = pygame.image.load("Textures\\Number 3.png")
Num4 = pygame.image.load("Textures\\Number 4.png")
Num5 = pygame.image.load("Textures\\Number 5.png")
Num6 = pygame.image.load("Textures\\Number 6.png")
Num7 = pygame.image.load("Textures\\Number 7.png")
Num8 = pygame.image.load("Textures\\Number 8.png")

ClosedCell = pygame.image.load("Textures\\closed_cell.png")
EmptyCell = pygame.image.load("Textures\\empty cell.png")

# THE FACES
NormalFace = pygame.image.load("Textures\\normal face.png")
LostFace = pygame.image.load("Textures\\lost face.png")
CoolFace = pygame.image.load("Textures\\cool face.png")


# THE MINES AND THE FLAG
Mine = pygame.image.load("Textures\\mine.png")
CrossedMine = pygame.image.load("Textures\\crossed mine.png")
Flag = pygame.image.load("Textures\\red flag.png")



def Draw_THE_Cell(TypeOfcell, size, x, y, Window):
    TypeOfcell = pygame.transform.scale(TypeOfcell, (size, size))
    Window.blit(TypeOfcell, (x,y))

def Draw_cells(FieldClean, FieldOpen, CurrentRow, CurrentColl, SquareX, SquareY, SquareSize, Window):

    if FieldClean[CurrentRow][CurrentColl] == ".":
        # cell is closed

        Draw_THE_Cell(ClosedCell, SquareSize, SquareX, SquareY, Window)
        
    else:
        # cell is openned

        if FieldClean[CurrentRow][CurrentColl] == FLAG:
            Draw_THE_Cell(Flag, SquareSize, SquareX, SquareY, Window)

        elif FieldClean[CurrentRow][CurrentColl] == "-":
            # cell is empty
            Draw_THE_Cell(EmptyCell, SquareSize, SquareX, SquareY, Window)

        elif FieldClean[CurrentRow][CurrentColl] == MIS_FLAG:
            Draw_THE_Cell(CrossedMine, SquareSize, SquareX, SquareY, Window)

        elif FieldOpen[CurrentRow][CurrentColl] != BOMB:
            Num = FieldClean[CurrentRow][CurrentColl]
            Num = NumberDistributor(Num)
            Draw_THE_Cell(Num, SquareSize, SquareX, SquareY, Window)

        elif FieldOpen[CurrentRow][CurrentColl] == BOMB:
            Draw_THE_Cell(Mine, SquareSize, SquareX, SquareY, Window)


def Draw_the_board(FieldClean, FieldOpen, ScreenWidth, StartX, StartY, Window):
    Rows = len(FieldOpen)
    Cols = len(FieldOpen[0])
    SquareSize = ScreenWidth // Cols

    for i in range(Rows):
        for j in range(Cols):
            X_for_square = StartX + j * SquareSize
            Y_for_square = StartY + i * SquareSize

            Draw_cells(FieldClean, FieldOpen, i, j, X_for_square, Y_for_square, SquareSize, Window)


def Draw_ChangeDifficulty(Difficulty, Font, Colour, sizex, sizey, screen_width, Window):

    #ClosedCell = pygame.transform.scale(EmptyCell, (sizex, sizey))
    # need to find a proper texture

    ChangeDifficulty = Font.render(Difficulty, True, Colour)

    x = 20
    y = 5
    #Window.blit(ClosedCell, (x,y))
    Window.blit(ChangeDifficulty, (x,y))

    
def BombCounter(Font, BombCounter, Colour, screen_width, Window):
    x = screen_width // 2 - 110
    Bombs = Font.render(f"{BombCounter:3d}", True, Colour)
    Window.blit(Bombs, (x, 5))

def draw_face(FaceState, size, screen_width, Window):
    if FaceState == "Cool":
        Face = CoolFace
    elif FaceState == "Lost":
        Face = LostFace
    else:
        Face = NormalFace
    
    x = screen_width//2 - 20
    y = 2.5
    Face = pygame.transform.scale(Face, (size, size))
    Window.blit(Face, (x,y))

    pass

def NumberDistributor(Num):
    if Num == "1":
        return Num1
    if Num == "2":
        return Num2
    if Num == "3":
        return Num3
    if Num == "4":
        return Num4
    if Num == "5":
        return Num5
    if Num == "6":
        return Num6
    if Num == "7":
        return Num7
    if Num == "8":
        return Num8