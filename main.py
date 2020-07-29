#Connect 4 Game
import numpy as np
import pygame
import pygame.freetype
import random
import threading
import time

pygame.init()

#Color scheme
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (251, 201, 61)
RED = (251,79,79)
BLUE = (108,192,229)

#Screen size
size = (700, 500)
screen = pygame.display.set_mode(size)

PLAYER_TURN, AI_TURN = 0, 1
state = AI_TURN
result = None
done = False

pygame.display.set_caption("Connect 4")
clock = pygame.time.Clock()
font = pygame.freetype.Font(None, 20)

RADIUS = 30
DIAMETER = RADIUS * 2
MARGIN = 10
X_OFFSET = 50
Y_OFFSET = 100
valid = False
grid = [[-1 for x in range(7)] for y in range(6)]

def turn(grid, state1):
    print('thinking very hard....')
    time.sleep(1)
    global result
    global state
    valid = False
    temp = random.randint(0, 6)
    while not valid:
        temp = random.randint(0, 6)
        print(temp)
        grid, valid = checkLastAvailable(grid, temp, state1)
    print('back to player...')
    result = temp
    
def checkLastAvailable(grid, col, state):
    for i in range(0, 6):
        if (grid[5 - i][col] == -1):
            grid[5 - i][col] = state
            return grid, True
    print("illegal move, retry please...")
    return grid, False

def checkWin(grid):
    hortWin, hortWho = checkHorizontalWin()
    if hortWin:
        return True, hortWho
    
    vertWin, vertWho = checkVerticalWin()
    if vertWin:
        return True, vertWho

    diagWin, diagWho = checkVerticalWin()
    if diagWin:
        return True, diagWho

    return False, -1

def checkHorizontalWin():
    for i in range(6):
        for j in range(4):
            if (grid[i][j] == 1 and grid[i][j+1] == 1 and grid[i][j+2] == 1 and grid[i][j+3] == 1):
                return True, 1
            if (grid[i][j] == 0 and grid[i][j+1] == 0 and grid[i][j+2] == 0 and grid[i][j+3] == 0):
                return True, 0

    return False, -1

def checkVerticalWin():
    for i in range(3):
        for j in range(7):
            if (grid[i][j] == 1 and grid[i+1][j] == 1 and grid[i+2][j] == 1 and grid[i+3][j] == 1):
                return True, 1
            if (grid[i][j] == 0 and grid[i+1][j] == 0 and grid[i+2][j] == 0 and grid[i+3][j] == 0):
                return True, 0
    
    for i in range(3):
        for j in range(3, 7):
            if (grid[i][j] == 1 and grid[i+1][j-1] == 1 and grid[i+2][j-2] == 1 and grid[i+3][j-3] == 1):
                return True, 1
            if (grid[i][j] == 0 and grid[i+1][j-1] == 0 and grid[i+2][j-2] == 0 and grid[i+3][j-3] == 0):
                return True, 0

    return False, -1
            
while not done:
    # Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if state == PLAYER_TURN:
                t = threading.Thread(target=turn, args=[grid, AI_TURN]).start()
                time.sleep(2)
                print(t)
                state = AI_TURN
                valid = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # User clicks the mouse. Get the position
            if state == AI_TURN:
                while valid == False:
                    pos = pygame.mouse.get_pos()
                    col = (pos[0] - Y_OFFSET) // (DIAMETER + MARGIN)
                    row = (pos[1] - X_OFFSET) // (DIAMETER + MARGIN)
                    grid, valid = checkLastAvailable(grid, col, PLAYER_TURN)
                    print("Click ", pos, "grid ", row, col, "grid ", grid, "valid", valid)
                state = PLAYER_TURN
                valid = False
                
    # --- Game logic should go here
    win, who = checkWin(grid)
    if win:
        print('game over')
        if (who == PLAYER_TURN):
            print('player won')
        elif (who == AI_TURN):
            print('ai won')
        done = True
    if state == PLAYER_TURN:
#         print('Player_turn')
        font.render_to(screen, (0, 0), 'Player turn. Click anything')
    elif state == AI_TURN:
#         print('AI_turn')
        font.render_to(screen, (0, 0), 'AI turn.')
    #Blue screen background
    screen.fill(BLUE)
    
    #Draw the pieces
    # [80, 140, 200, 260, 320, 380, 440]
    for row in range(0, 6):
        for col in range(0, 7):
            if (grid[row][col] == -1):
                pygame.draw.circle(screen, WHITE, (col*(DIAMETER + MARGIN) + (MARGIN + RADIUS + Y_OFFSET), row*(DIAMETER + MARGIN) + (MARGIN + RADIUS + X_OFFSET)), RADIUS, 0)
            elif (grid[row][col] == PLAYER_TURN):
                pygame.draw.circle(screen, RED, (col*(DIAMETER + MARGIN) + (MARGIN + RADIUS + Y_OFFSET), row*(DIAMETER + MARGIN) + (MARGIN + RADIUS + X_OFFSET)), RADIUS, 0)
            elif (grid[row][col] == AI_TURN):
                pygame.draw.circle(screen, YELLOW, (col*(DIAMETER + MARGIN) + (MARGIN + RADIUS + Y_OFFSET), row*(DIAMETER + MARGIN) + (MARGIN + RADIUS + X_OFFSET)), RADIUS, 0)
    # pygame.draw.rect(screen, BLACK, (Y_OFFSET, X_OFFSET, 560 + Y_OFFSET, 440 + X_OFFSET), 1)
    # Updates the screen
    pygame.display.flip()
    
    # 60 fps
    clock.tick(60)
 
# Close the window and quit.
pygame.quit()

