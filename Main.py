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
SQUARE_PRIMARY_COLOUR =(169,96,0)
SQUARE_SECONDARY_COLOUR = (139,82,8)

CHANGE_DIFFICULTY = (151, 97, 3)
CHANGE_DIFFICULTY_HEIGHT = 40
CHANGE_DIFFICULTY_WIDTH = 100


WHITE = (255,255,255)
RED = (255, 0, 0)
BLACK = (0,0,0)
BROWNISH = (145, 100, 10)

# clock
font_for_clock = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

# my window
Screen_Heigth = 546
Screen_Width = 496
MyWindow = pygame.display.set_mode((Screen_Width, Screen_Heigth))
pygame.display.set_caption("Minesweeper")

# Gamemode and primary field creation
Gamemode = "Medium"
Difficulty_change_Rect = pygame.Rect(30, 5, CHANGE_DIFFICULTY_WIDTH, CHANGE_DIFFICULTY_HEIGHT)
FieldClean, FieldOpen, BombCounter = Logic.FieldManage("Medium", True)

# timer stuff
playing = False
start_time = 0
elapsed_time = 0
seconds = 0

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
                        
                        FieldClean, FieldOpen, BombCounter = Logic.FieldManage(Gamemode, primary)
                        playing = True
                        start_time = pygame.time.get_ticks()

                    Lost, BombCounter = Logic.Replacing_cells_in_FieldClean(LEFT,MouseCoord, START_X, START_Y, SquareSize)
            if Difficulty_change_Rect.collidepoint(MouseCoord):
                Gamemode, Screen_Heigth, Screen_Width, SquareSize = Logic.ChangingDifficulty(Gamemode, Screen_Heigth, Screen_Width, SquareSize)
                playing = False
                Lost = False
                PlayableRect = pygame.Rect(START_X, START_Y, Screen_Width, Screen_Width)
                FieldClean, FieldOpen, BombCounter = Logic.FieldManage(Gamemode, primary)
                pygame.display.set_mode((Screen_Width,Screen_Heigth))


        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT:
            MouseCoord = pygame.mouse.get_pos()
            if PlayableRect.collidepoint(MouseCoord):
                if Lost == False:
                    if playing == False:
                        # for the timer and first openned cell
                        primary = False
                        FieldClean, FieldOpen, BombCounter = Logic.FieldManage(2, primary)
                        playing = True
                        start_time = pygame.time.get_ticks()
                    Lost, BombCounter = Logic.Replacing_cells_in_FieldClean(RIGHT, MouseCoord, START_X, START_Y, SquareSize)
        


    Graphics.Draw_the_board(FieldClean, FieldOpen, Screen_Width, START_X, START_Y, WHITE, SQUARE_PRIMARY_COLOUR, SQUARE_SECONDARY_COLOUR, MyWindow)

    # drawing bomb counter 
    Graphics.BombCounter(BombCounter, WHITE, MyWindow)

    # change difficulty button
    Graphics.Draw_ChangeDifficulty(Gamemode, WHITE, CHANGE_DIFFICULTY_WIDTH, CHANGE_DIFFICULTY_HEIGHT, 30, 5, CHANGE_DIFFICULTY, MyWindow)

    
    Won = Logic.WinCheck(Lost) # doen't work 
    if Won:
        Lost == True # :)
        

    # timer settings
    if playing == True and Lost == False:
        elapsed_time = pygame.time.get_ticks() - start_time
        seconds = (elapsed_time // 1000)
    if seconds == 999: # needs to be developed
        Lost = True

    Timer = font_for_clock.render(f"{seconds:03d}", True, WHITE)
    MyWindow.blit(Timer, (280, 0))


    # should remain in the end
    pygame.display.flip()
    MyWindow.fill(BLACK)
    clock.tick(60)
pygame.quit