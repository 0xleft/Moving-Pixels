import pygame
import time
from settings import *
import threading
import math
import numpy

dtimeStart = time.perf_counter()
pygame.init()
clock = pygame.time.Clock()
gameDisplay = pygame.display.set_mode((PYGAME_WIDTH,PYGAME_HEIGHT))

FPS = 60
menu = pygame.image.load('menu.jpg')

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

def drawGrid():
    y = 0
    for i in grid:
        x=0
        for j in i: #we have singular block 0 = white 1= black
            if j == 1:
                rect = pygame.Rect(x,y,BLOCKSIZE,BLOCKSIZE)
                pygame.draw.rect(gameDisplay, [0,0,0], rect, 10)
            if j == 0:
                rect = pygame.Rect(x,y,BLOCKSIZE,BLOCKSIZE)
                pygame.draw.rect(gameDisplay, [255,255,0], rect, 10)
            x+=BLOCKSIZE
        y+=BLOCKSIZE
        

def getFirstDigit(num):
    digits = int(math.log10(num))
    first_digit = int(num / pow(10, digits))
    return first_digit


def findGrid(mousepos):
    mousepos = [int(mousepos[0]/BLOCKSIZE), int(mousepos[1]/BLOCKSIZE)]
    print(mousepos, 'changes this grid point')
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
    tempgrid = numpy.random.randint(0,1,GRID_SHAPE).tolist()
    for row in grid:
        x=0
        for cell in row:
            neighbours = countNeighbours([x,y])
            if cell == 1 and neighbours < 2:
                tempgrid[y][x] = 0 # underpopulation
            if cell == 1 and neighbours in range(2,4):
                tempgrid[y][x] = 1 # lives
            if cell == 1 and neighbours > 3:
                tempgrid[y][x] = 0 # overpopulation
            if cell == 0 and neighbours == 3:
                tempgrid[y][x] = 1
            x+=1
        y+=1
    return tempgrid

changing = False
threading.Thread(target=count_seconds, name='counting_seconds_thread').start()
while True:
    mousepos = pygame.mouse.get_pos()
    gameDisplay.fill(BACKGROUND_COLOR)


    dtime = time.perf_counter() - dtimeStart
    
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            changing = True
        if event.type == pygame.MOUSEBUTTONUP:
            changing = False
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
            if event.key == pygame.K_SPACE:
                if started_playing == True:
                    started_playing = False
                    FPS = 60
                else:
                    started_playing = True
                    FPS = 4
            if event.key == pygame.K_HOME:
                grid =numpy.random.randint(0,2,GRID_SHAPE).tolist()
            if event.key == pygame.K_d:
                FPS += 3
                print(f'FPS: {FPS}')
            if event.key == pygame.K_a:
                FPS -= 3
                print(f'FPS: {FPS}')
    

    #------------------#
    if changing == True:
        changes = findGrid(mousepos)
        if grid[changes[1]][changes[0]] == 1:
            grid[changes[1]][changes[0]] = 0
        else:
            grid[changes[1]][changes[0]] = 1

    if started_playing == True:
        grid = simulate()
    drawGrid()
    #if not started_playing:
    #    gameDisplay.blit(menu, (0,0))

    #pygame.draw.circle(gameDisplay, [255,255,0], (255,255), dtime*10, 2)

    #------------------#

    pygame.display.update()