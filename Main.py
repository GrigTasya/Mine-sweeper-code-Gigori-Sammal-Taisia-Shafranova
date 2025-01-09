# misweeper main

import pygame, sys
import Logic
import Graphics

pygame.init()

# types of mouse clicks
RIGHT = 3
LEFT = 1

# not sure why it is needed here
FLAG = ">"
BOMB = "B"

# for the placement of squares
START_X = 0
START_Y = 50

# colours for things
CHANGE_DIFFICULTY = (151, 97, 3)
CHANGE_DIFFICULTY_HEIGHT = 40
CHANGE_DIFFICULTY_WIDTH = 100

WHITE = (255, 255, 255)
GRAY = (192,192,192)
RED = (220, 0, 0)
BLACK = (0,0,0)
BROWNISH = (145, 100, 10)

# clock

clock = pygame.time.Clock()

# my window
Screen_Heigth = 546
Screen_Width = 496
MyWindow = pygame.display.set_mode((Screen_Width, Screen_Heigth))
pygame.display.set_caption("Minesweeper")

# stopwatch coords
Y_for_STOPWATCH = 5

# Gamemode and primary field creation
Gamemode = "Medium"
Difficulty_change_Rect = pygame.Rect(20, 5, CHANGE_DIFFICULTY_WIDTH, CHANGE_DIFFICULTY_HEIGHT)
FieldClean, FieldOpen, BombCounter = Logic.FieldManage("Medium", True)

# font
Font = pygame.font.Font("Font\\digital-7.ttf", 50)



# timer stuff
playing = False
start_time = 0
elapsed_time = 0
seconds = 0

# Face stuff
FaceSize = 45
Face_rect = pygame.Rect(Screen_Width/2 - FaceSize/2, 2.5, FaceSize,FaceSize)
FaceState = "Normal"



# playable rect
SquareSize = 31
PlayableRect = pygame.Rect(START_X, START_Y, Screen_Width, Screen_Width)

primary = False
Lost = False
Won = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
            MouseCoord = pygame.mouse.get_pos()
            if PlayableRect.collidepoint(MouseCoord):
                if Lost == False:
    
                    if playing == False:
                        # for the timer and first openned cell
                        
                        MouseTuple = Logic.GettingMousePos(MouseCoord, START_X, START_Y, SquareSize)
                        FieldClean, FieldOpen, BombCounter = Logic.FieldManage(Gamemode, primary, MouseTuple)

                        playing = True
                        start_time = pygame.time.get_ticks()

                    Lost, BombCounter = Logic.Replacing_cells_in_FieldClean(LEFT, MouseCoord, START_X, START_Y, SquareSize, BombCounter, FieldOpen, FieldClean)
                    if Lost == True and Won == False:
                        FaceState = "Lost"

            if Difficulty_change_Rect.collidepoint(MouseCoord):
                Gamemode, Screen_Heigth, Screen_Width, SquareSize = Logic.ChangingDifficulty(Gamemode, Screen_Heigth, Screen_Width, SquareSize)
                playing = False
                Lost = False
                FaceState = "Normal"
                Face_rect = pygame.Rect(Screen_Width/2 - FaceSize/2, 2.5, FaceSize,FaceSize)
                PlayableRect = pygame.Rect(START_X, START_Y, Screen_Width, Screen_Width)
                FieldClean, FieldOpen, BombCounter = Logic.FieldManage(Gamemode, primary)
                pygame.display.set_mode((Screen_Width,Screen_Heigth))

            if Face_rect.collidepoint(MouseCoord):
                playing = False
                Lost = False
                seconds = 0
                FaceState = "Normal"
                FieldClean, FieldOpen, BombCounter = Logic.FieldManage(Gamemode, primary)
                

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT:
            MouseCoord = pygame.mouse.get_pos()
            if PlayableRect.collidepoint(MouseCoord):
                if Lost == False:
                    if playing == False:
                        # for the timer and first openned cell
                        primary = False
                        FieldClean, FieldOpen, BombCounter = Logic.FieldManage("Medium", primary)
                        playing = True
                        start_time = pygame.time.get_ticks()
                    Lost, BombCounter = Logic.Replacing_cells_in_FieldClean(RIGHT, MouseCoord, START_X, START_Y, SquareSize, BombCounter, FieldOpen, FieldClean)
        


    Graphics.Draw_the_board(FieldClean, FieldOpen, Screen_Width, START_X, START_Y, MyWindow)

    # drawing bomb counter 
    Graphics.BombCounter(Font, BombCounter, RED, Screen_Width, MyWindow)

    # change difficulty button
    Graphics.Draw_ChangeDifficulty(Gamemode, Font, WHITE, MyWindow)


    
    Won = Logic.WinCheck(Lost, BombCounter, FieldOpen, FieldClean)
    if Won:
        Logic.StoreDecision(seconds, Gamemode)
        FaceState = "Cool"
        Lost = True # :)

    # draw face
    Graphics.draw_face(FaceState, FaceSize, Screen_Width, MyWindow)



    # timer settings
    if playing == True and Lost == False:
        elapsed_time = pygame.time.get_ticks() - start_time
        seconds = (elapsed_time // 1000)
    if seconds == 999: # needs to be developed
        Lost = True

    Timer = Font.render(f"{seconds:03d}", True, RED)
    X_for_STOPWATCH = Screen_Width // 2 + 50
    MyWindow.blit(Timer, (X_for_STOPWATCH, Y_for_STOPWATCH))


    # should remain in the end
    pygame.display.flip()
    MyWindow.fill(BLACK)
    clock.tick(60)
pygame.quit