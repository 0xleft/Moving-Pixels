import pygame
import time
from settings import *
import threading
import math
import numpy
import random


dtimeStart = time.perf_counter()
pygame.init()
clock = pygame.time.Clock()
gameDisplay = pygame.display.set_mode((PYGAME_WIDTH,PYGAME_HEIGHT))

changes = []
all_changes = []
FPS = 60

blinked = False
stopping = False
started_playing = False


def count_seconds():
    last = time.perf_counter()
    count = 0
    while not stopping:
        if time.perf_counter() - last >= 1:
            last = time.perf_counter()
            count+=1
            #print(count)


grid = numpy.random.randint(0,1,GRID_SHAPE).tolist()
print(len(grid), len(grid[0]), '<--------shape of the grid')

def detectEmptyEdnges(boys):
    if 1 in boys[0]:
        return False # edges arent empty
    if 1 in boys[-1]:
        return False # edges arent empty
    for i in range(len(boys)):
        if boys[i][0] == 1:
            return False
        if boys[i][-1] == 1:
            return False
    return True

boys = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]*10

print(detectEmptyEdnges(boys))


def updateGrid():
    global changes, all_changes
    print(len(changes),changes)
    for i in changes:
        y,x,cell = i
        if cell == 1:
            rect = pygame.Rect(x*BLOCKSIZE,y*BLOCKSIZE,BLOCKSIZE,BLOCKSIZE)
            pygame.draw.rect(gameDisplay, [0,0,0], rect, 100)
        if cell == 0:
            rect = pygame.Rect(x*BLOCKSIZE,y*BLOCKSIZE,BLOCKSIZE,BLOCKSIZE)
            pygame.draw.rect(gameDisplay, [255,255,255], rect, 100)
        grid[y][x] = cell
    all_changes.append(changes)
    changes=[]


def getFirstDigit(num):
    digits = int(math.log10(num))
    first_digit = int(num / pow(10, digits))
    return first_digit


def findGrid(mousepos):
    mousepos = [int(mousepos[0]/BLOCKSIZE), int(mousepos[1]/BLOCKSIZE)]
    return mousepos


def countNeighbours(cell):
    neighbors = []
    # going to do one by one

#top row
    try:
        neighbors.append(grid[cell[1]-1][cell[0]-1])
    except IndexError:
        pass
    try:
        neighbors.append(grid[cell[1]-1][cell[0]])
    except IndexError:
        pass
    try:
        neighbors.append(grid[cell[1]-1][cell[0]+1])
    except IndexError:
        pass

#main row
    try:
        neighbors.append(grid[cell[1]][cell[0]-1])
    except IndexError:
        pass
    try:
        neighbors.append(grid[cell[1]][cell[0]+1])
    except IndexError:
        pass

#bottom row
    try:
        neighbors.append(grid[cell[1]+1][cell[0]-1])
    except IndexError:
        pass
    try:
        neighbors.append(grid[cell[1]+1][cell[0]])
    except IndexError:
        pass
    try:
        neighbors.append(grid[cell[1]+1][cell[0]+1])
    except IndexError:
        pass
    
    count = neighbors.count(1)
    return count


def simulate():
    y = 0
    for row in grid:
        x=0
        for cell in row:
            neighbours = countNeighbours([x,y])
            if cell == 1 and neighbours < 2:
                changes.append([y,x,0]) # underpopulation
            if cell == 1 and neighbours in range(2,4):
                changes.append([y,x,1])
            if cell == 1 and neighbours > 3:
                changes.append([y,x,0])
            if cell == 0 and neighbours == 3:
                changes.append([y,x,1])
            x+=1
        y+=1


gameDisplay.fill(BACKGROUND_COLOR)
changing = False
threading.Thread(target=count_seconds, name='counting_seconds_thread').start()
while True:

    mousepos = pygame.mouse.get_pos() # get mouse position
     # refresh
    dtime = time.perf_counter() - dtimeStart
    
    clock.tick(FPS)


    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            changes_m = findGrid(mousepos)
            if grid[changes_m[1]][changes_m[0]] == 1:
                changes.append([changes_m[1],changes_m[0], 0])
            else:
                changes.append([changes_m[1],changes_m[0], 1])
            print(changes_m,changes)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                stopping = True
                pygame.quit()
                threads = threading.enumerate()
                for i in threads:
                    try:
                        i.join()
                    except RuntimeError:
                        print(f'cannot join {i}')
                break
            #if event.key == pygame.K_HOME:
            #    grid =numpy.random.randint(0,2,GRID_SHAPE).tolist()
            if event.key == pygame.K_SPACE:
                if started_playing == True:
                    started_playing=False
                else:
                    started_playing=True


    
    if started_playing == True:
        simulate()

    if len(changes) != 0:
        updateGrid()
    
    try:
        if numpy.array_equal(all_changes[-1], all_changes[-3]):
            started_playing = False
            print(len(all_changes))
            print('repetition')
    except:
        print('not enought updates')


    #if not started_playing:
    #    gameDisplay.blit(menu, (0,0))

    #pygame.draw.circle(gameDisplay, [255,255,0], (255,255), dtime*10, 2)

    #------------------#

    pygame.display.update()
