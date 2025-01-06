#minesweeper logic
import random

BOMB = "B"
FLAG = ">"
MIS_FLAG = "<"
RIGHT = 3
LEFT = 1

global BoardWidth, BoardHeight, AmountOfBombs
global Top5List
global BombCounter
global FieldClean, FieldOpen

Top5List = []



#___________________THE CREATION OF THE FIELD BLOCK________________________________
def FieldManage(Difficulty, primary, *Mousecoords): # Main subroutine for creating fields and placing the bombs
    global FieldClean, FieldOpen, AmountOfBombs, BombCounter, BoardWidth, BoardHeight
    if Difficulty == "Easy":
        BoardWidth, BoardHeight, AmountOfBombs = 9,9,10
    if Difficulty == "Medium":
        BoardWidth, BoardHeight, AmountOfBombs = 16,16,40
    if Difficulty == "Hard":
        BoardWidth, BoardHeight, AmountOfBombs = 30,16,99

    BombCounter = AmountOfBombs
    FieldClean, FieldOpen = CreatingField()
    
    if primary == False:
        for count in range(0, AmountOfBombs): # Placing bombs
            PlaceItem(Mousecoords)
        
        for y in range(0, BoardHeight):
            for x in range(0, BoardWidth):
                if FieldOpen[y][x] != BOMB:
                    FieldOpen[y][x] = CheckSurroundingCells(y, x)

    return FieldClean, FieldOpen, BombCounter
    

def CreatingField(): 
    FieldClean = [["." for i in range(BoardWidth)] for j in range(BoardHeight)]
    FieldOpen = [["-" for i in range(BoardWidth)] for j in range(BoardHeight)]
    return FieldClean, FieldOpen


def GetRandom(): 
    return random.randint(0, BoardWidth - 1), random.randint(0, BoardHeight - 1)

def PlaceItem(Mousecoords):
    RandomY, RandomX = GetRandom()

    while FieldOpen[RandomX][RandomY] == BOMB or FieldOpen[RandomX][RandomY] == Mousecoords:
        RandomY, RandomX = GetRandom()
    if FieldOpen[RandomX][RandomY] != BOMB:
        FieldOpen[RandomX][RandomY] = BOMB

def CheckRange(Row, Column):
    StartRow = max(0, Row - 1)
    EndRow = min(BoardHeight - 1, Row + 1)
    StartColumn = max(0, Column - 1)
    EndColumn = min(BoardWidth - 1, Column + 1)
    return StartRow, EndRow, StartColumn, EndColumn

def CheckSurroundingCells(row, column):
    Neighbouring = 0
    StartRow, EndRow, StartColumn, EndColumn = CheckRange(row, column)

    for R in range(StartRow, EndRow+1):
        for C in range(StartColumn, EndColumn+1):
            if FieldOpen[R][C] == BOMB:
                Neighbouring  += 1
    if Neighbouring == 0:
        return "-" 

    return str(Neighbouring)
#___________________THE END OF THE CREATION OF THE FIELD BLOCK____________________________



#___________________DISPLAYING THE FIRST TURN BLOB BLOCK__________________________________

def find_connected_0_value_cells(i,j):

    FieldClean[i][j] = FieldOpen[i][j]

    if FieldOpen[i][j] == "-":

        s = (i, j + 1)
        t = (i, j - 1)
        u = (i - 1, j - 1)
        v = (i - 1, j)
        w = (i - 1, j + 1)
        x = (i + 1, j - 1)
        y = (i + 1, j)
        z = (i + 1, j + 1)
        neighboring = s,t,u,v,w,x,y,z
        for Cell in neighboring: 
            if check_coord_values(Cell[0], Cell[1]):
                if FieldClean[Cell[0]][ Cell[1]] != FieldOpen[Cell[0]][ Cell[1]]:
                    find_connected_0_value_cells(Cell[0], Cell[1])
        

def check_coord_values(a,b):

    if a == -1 or a >= BoardHeight:
        return False
    if b == -1 or b >= BoardWidth:
        return False
    else:
        return True
#___________________THE END OF DISPLAYING THE FIRST TURN BLOB BLOCK_______________________



#___________________THE STORE BLOCK_______________________________________________________
def Storemain(Score, Gamemode): # needs WinCheck to work properly to work (It currently doesn't )
    if StoreDecision(Score, Gamemode):
        StoreProcedure(Score, Gamemode)

def StoreProcedure(Score, Gamemode):
    global Top5List
    TopList = open("Top5Score", "w")
    for record in Top5List:
        TopList.write(record)
    TopList.close

def StoreDecision(Score, Gamemode):
    global Top5List
    filename = f"{Gamemode}Top5Score"
    open(filename, "a+").close # It should automatically create 3 files for storing top 5 time

    TopList = open(filename, "r+")
    Top5List = TopList.readlines()
    TopList.close()
    NewList = []
    for record in Top5List:
        NewList.append(record)

    for i in range(len(Top5List)): # not sure if it works
        Num = int(Top5List[i].replace("\n", ""))
        if Score == Num:
            return False
        elif Score < Num:
            NewList[i] = f"{Score}\n"
            break
    for j in range(0,4):
        if NewList[j] != Top5List[j]:
            NewList[j+1] = Top5List[j]      
    Top5List = NewList
        
    return True
#___________________THE END OF THE STORE BLOCK____________________________________________

def GettingMousePos(Mousecoords, START_X, START_Y, SquareSize):
    x, y = Mousecoords[0], Mousecoords[1]
    SquareNumHor = int((x - START_X) // SquareSize)
    #print(SquareNumHor)
    SquareNumVer =  int((y - START_Y) // SquareSize)
    #print(SquareNumVer)
    return SquareNumVer, SquareNumHor

def Replacing_cells_in_FieldClean(Side, Mousecoords, START_X, START_Y, SquareSize):
    global BombCounter
    SquareNumVer, SquareNumHor = GettingMousePos(Mousecoords, START_X, START_Y, SquareSize)
    

    cell = FieldOpen[SquareNumVer][SquareNumHor]
    if Side == LEFT:
        if FieldClean[SquareNumVer][SquareNumHor] == FLAG:
            return False, BombCounter # can't open the cell marked with a flag
        elif cell == BOMB:
            BombReveal()
            return True, BombCounter
        elif cell == "-":
            find_connected_0_value_cells(SquareNumVer,SquareNumHor)
        else:    
            FieldClean[SquareNumVer][SquareNumHor] = cell

    elif Side == RIGHT:
        if FieldClean[SquareNumVer][SquareNumHor] == FLAG:
            FieldClean[SquareNumVer][SquareNumHor] = "."
            BombCounter += 1 
        else:
            if Can_place_flags(SquareNumVer,SquareNumHor):
                FieldClean[SquareNumVer][SquareNumHor] = FLAG
                BombCounter -= 1

    return False, BombCounter
            


def BombReveal():
    for row in range(len(FieldClean)):
        for col in range(len(FieldClean[row])):
            if FieldClean[row][col] == FLAG and FieldOpen[row][col] != BOMB:
                FieldClean[row][col] = MIS_FLAG
            elif FieldClean[row][col] != FLAG and FieldOpen[row][col] == BOMB:
                FieldClean[row][col] = BOMB


def Can_place_flags(x,y):
    cell = FieldClean[x][y]
    if cell >= "1" and cell <= "8":
        return False
    elif cell == "-":
        return False
    elif cell == ".":
        return True
    
def ChangingDifficulty(Difficulty, Screen_Heigth, Screen_Width, SquareSize):
    if Difficulty == "Easy": # Оч тупо, училка не оценит
        Difficulty = "Medium"
        Screen_Heigth = 546
        Screen_Width = 496
        SquareSize = 31
    
    elif Difficulty == "Medium":
        Difficulty = "Hard"
        Screen_Heigth = 530
        Screen_Width = 900
        SquareSize = 30
    else:
        Difficulty = "Easy"
        Screen_Heigth = 545
        Screen_Width = 495
        SquareSize = 55 
    
    return Difficulty, Screen_Heigth, Screen_Width, SquareSize

def WinCheck(Lost): # doesn't work
    if Lost:
        return False
    for row in range(len(FieldClean)):
        for col in range(len(FieldClean[row])):
            if FieldClean[row][col] == ".":
                return False
    return True