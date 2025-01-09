#minesweeper logic
import random
import os

BOMB = "B"
FLAG = ">"
MIS_FLAG = "<"
RIGHT = 3
LEFT = 1



#___________________THE CREATION OF THE FIELD BLOCK________________________________
def FieldManage(Difficulty, primary, Mousecoords=0): # Main subroutine for creating fields and placing the bombs
    if Difficulty == "Easy":
        BW, BH, AoB = 9,9,10
    if Difficulty == "Medium":
        BW, BH, AoB = 16,16,40
    if Difficulty == "Hard":
        BW, BH, AoB = 30,16,99

    BombCounter = AoB
    FieldClean, FieldOpen = CreatingField(BW, BH)
    
    if primary == False:
        for count in range(0, AoB): # Placing bombs
            PlaceItem(Mousecoords, BW, BH, FieldOpen)
        
        for x in range(0, BW):
            for y in range(0, BH):
                if FieldOpen[y][x] != BOMB:
                    FieldOpen[y][x] = CheckSurroundingCells(y, x, FieldOpen, BW, BH)

    return FieldClean, FieldOpen, BombCounter
    

def CreatingField(BW, BH): 
    FieldClean = [["." for i in range(BW)] for j in range(BH)]
    FieldOpen = [["-" for i in range(BW)] for j in range(BH)]
    return FieldClean, FieldOpen


def GetRandom(BW,BH): 
    return random.randint(0, BH - 1), random.randint(0, BW - 1)

def PlaceItem(Mousecoords, BW, BH, FieldOpen):
    RandomX, RandomY = GetRandom(BW, BH)

    #randomTuple = RandomX,RandomY
    #or randomTuple == Mousecoords
    while FieldOpen[RandomX][RandomY] == BOMB:
        RandomX, RandomY = GetRandom(BW, BH)

    FieldOpen[RandomX][RandomY] = BOMB

def CheckRange(Row, Column, BW, BH):
    StartRow = max(0, Row - 1)
    EndRow = min(BH - 1, Row + 1)
    StartColumn = max(0, Column - 1)
    EndColumn = min(BW - 1, Column + 1)
    return StartRow, EndRow, StartColumn, EndColumn

def CheckSurroundingCells(row, column, FieldOpen, BW, BH):
    Neighbouring = 0
    StartRow, EndRow, StartColumn, EndColumn = CheckRange(row, column, BW, BH)

    for R in range(StartRow, EndRow+1):
        for C in range(StartColumn, EndColumn+1):
            if FieldOpen[R][C] == BOMB:
                Neighbouring  += 1
    if Neighbouring == 0:
        return "-" 

    return str(Neighbouring)
#___________________THE END OF THE CREATION OF THE FIELD BLOCK____________________________



#___________________DISPLAYING THE FIRST TURN BLOB BLOCK__________________________________

def find_connected_0_value_cells(i,j, BW, BH, FieldOpen, FieldClean):

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
            if check_coord_values(Cell[0], Cell[1], BW, BH):
                if FieldClean[Cell[0]][ Cell[1]] != FieldOpen[Cell[0]][ Cell[1]]:
                    find_connected_0_value_cells(Cell[0], Cell[1],BW, BH, FieldOpen, FieldClean)
        

def check_coord_values(a,b, BW, BH):

    if a == -1 or a >= BW:
        return False
    if b == -1 or b >= BH:
        return False
    else:
        return True
#___________________THE END OF DISPLAYING THE FIRST TURN BLOB BLOCK_______________________



#___________________THE STORE BLOCK_______________________________________________________
def StoreProcedure(Top5List, Gamemode):
    filename = f"{Gamemode}Top5Score"
    filepath = os.path.join("Top_5_time", filename)

    TopList = open(filepath, "w")
    for record in Top5List:
        TopList.write(record)
    TopList.close

def StoreDecision(Score, Gamemode):
    Top5List = []
    filename = f"{Gamemode}Top5Score"
    filepath = os.path.join("Top_5_time", filename)
    if not os.path.exists("Top_5_time"):
        os.makedirs("Top_5_time")

    create = open(filepath, "a+") # It should automatically create 3 files for storing top 5 time
    create.close
    
    TopList = open(filepath, "r+")
    Top5List = TopList.readlines()
    TopList.close()
    
    if len(Top5List) == 0:
        list  = [f"{Score}\n"]
        for i in range(4):
            list.append("999\n")

        create = open(filepath, "r+")    
        create.writelines(list)
        create.close



    NewList = []
    for record in Top5List:
        NewList.append(record)

    for i in range(len(Top5List)): # not sure if it works
        Num = int(Top5List[i].replace("\n", ""))

        if Score < Num:
            NewList[i] = f"{Score}\n"
            break
    for j in range(len(Top5List)-1):
        if NewList[j] != Top5List[j]:
            NewList[j+1] = Top5List[j]      
    Top5List = NewList
        
    StoreProcedure(Top5List, Gamemode)
#___________________THE END OF THE STORE BLOCK____________________________________________

def GettingMousePos(Mousecoords, START_X, START_Y, SquareSize):
    x, y = Mousecoords[0], Mousecoords[1]
    SquareNumHor = int((x - START_X) // SquareSize)
    #print(SquareNumHor)
    SquareNumVer =  int((y - START_Y) // SquareSize)
    #print(SquareNumVer)
    return SquareNumVer, SquareNumHor

def Replacing_cells_in_FieldClean(Side, Mousecoords, START_X, START_Y, SquareSize, BombCounter, FieldOpen, FieldClean):
    SquareNumVer, SquareNumHor = GettingMousePos(Mousecoords, START_X, START_Y, SquareSize)
    BW = len(FieldClean)
    BH = len(FieldClean[0])

    cell = FieldOpen[SquareNumVer][SquareNumHor]
    if Side == LEFT:
        if FieldClean[SquareNumVer][SquareNumHor] == FLAG:
            return False, BombCounter # can't open the cell marked with a flag
        elif cell == BOMB:
            BombReveal(FieldOpen, FieldClean)
            return True, BombCounter
        elif cell == "-":
            find_connected_0_value_cells(SquareNumVer,SquareNumHor, BW, BH, FieldOpen, FieldClean)
        else:    
            FieldClean[SquareNumVer][SquareNumHor] = cell

    elif Side == RIGHT:
        if FieldClean[SquareNumVer][SquareNumHor] == FLAG:
            FieldClean[SquareNumVer][SquareNumHor] = "."
            BombCounter += 1 
        else:
            if Can_place_flags(SquareNumVer,SquareNumHor, FieldClean):
                FieldClean[SquareNumVer][SquareNumHor] = FLAG
                BombCounter -= 1

    return False, BombCounter
            


def BombReveal(FieldOpen, FieldClean):
    for row in range(len(FieldClean)):
        for col in range(len(FieldClean[row])):
            if FieldClean[row][col] == FLAG and FieldOpen[row][col] != BOMB:
                FieldClean[row][col] = MIS_FLAG
            elif FieldClean[row][col] != FLAG and FieldOpen[row][col] == BOMB:
                FieldClean[row][col] = BOMB


def Can_place_flags(x,y, FieldClean):
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


def WinCheck(Lost, BombCounter, FieldOpen, FieldClean):
    if Lost:
        return False 
    for row in range(len(FieldClean)):
        for col in range(len(FieldClean[row])):
            if FieldClean[row][col] == "." and FieldOpen[row][col] != BOMB:
                return False
    if BombCounter == 0:
        return True