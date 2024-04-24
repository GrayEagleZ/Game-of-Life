import pygame, sys
import numpy as np
from pygame.locals import *

#define some basic colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)

#create window size variables
WINDOW_HEIGHT= 736
WINDOW_WIDTH = 1024
WINDOW_SIZE = [WINDOW_WIDTH, WINDOW_HEIGHT]

#decide the size of the cells
CELL_WIDTH = 16
CELL_HEIGHT = 16
CELL_MARGIN = 1

#see how many cells will need to go into the array
NUM_HOR_CELLS = int(WINDOW_HEIGHT / CELL_HEIGHT)
NUM_VERT_CELLS = int(WINDOW_WIDTH / CELL_WIDTH)


#Start Pygame
pygame.init()

#Name the window
pygame.display.set_caption("Game of Life")

#initialize the clock variable for Frame rate
clock = pygame.time.Clock()

#used to find the number of alive cells around the cell sent into the function
def population_check(grid, row, col):
    cell_pop = 0
    
    for i in range(-1, 2):
        for j in range(-1, 2):

            #should NOT check if current cell is alive      should NOT check outside of array
            if not (not i and not j) and row + i < len(grid) and col + j < len(grid[row]):  #cells will not leave the screen because of this
                cell_pop += grid[row + i][col + j]

    return cell_pop
                
            


def main():
    global SCREEN
    global PAUSED
    PAUSED = True
    
    #create the screen 
    SCREEN = pygame.display.set_mode(WINDOW_SIZE)
    #fill the background
    SCREEN.fill(WHITE)

    
    #create Grid
    grid = []
    #fill the grid and make it 2D
    for row in range(NUM_HOR_CELLS):
        grid.append([]) #makes it 2D
        for column in range (NUM_VERT_CELLS):
           grid[row].append(0)  #all the cells start dead
        
    #font for cell's neighbors
    font = pygame.font.Font('freesansbold.ttf', 10)

    #create infinite loop
    running = True
    while running:
        
        #input handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                
                row = pos[1] // (CELL_WIDTH + CELL_MARGIN)
                column = pos[0] // (CELL_HEIGHT + CELL_MARGIN)
                
                #switches alive and dead cells
                if grid[row][column] == 0:
                    grid[row][column] = 1
                else:
                    grid[row][column] = 0     
                #shows what cell was clicked               
                print("Click ", pos, "Grid coordinates: ", row, column)
                
            #pauses and unpauses game
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                PAUSED = not PAUSED
                
        #create a grid copy of this frame (will be used to compare to the next frame)
        copy_grid = np.copy(grid)
  
        #change the next frame and using the cells from the current one
        #This ensures that all cells are correctly changed using the proper data instead of a changing data set
        for row in range(len(grid)):
            for column in range(len(grid[0])):
                cell_pop = population_check(grid, row, column)
                                     
                #The next frame should be created in comparison to the current one 
                if not PAUSED:
                    if grid[row][column] == 1:
                        if cell_pop < 2 or cell_pop > 3:        #if an alive cell is overpopulated or underpopulated it will die
                               copy_grid[row][column] = 0   
                        else:
                            copy_grid[row][column] = 1             #if it has the proper number of cells, it should continue, this is only here for redundancy
                    if grid[row][column] == 0:
                        if cell_pop == 3:                           #if a dead cell is surrounded by 3 cells, it will come alive (reproduction)
                            copy_grid[row][column] = 1 
                            
        #move to the next frame            
        grid = np.copy(copy_grid)
        
        for row in range(len(grid)):
            for column in range(len(grid[0])):

                if grid[row][column] == 1:
                    color = WHITE
                else:                               #color the cells based on alive / dead
                    color = BLACK
                pygame.draw.rect(SCREEN,    #Draw the cells
                                 color,
                                 [(CELL_MARGIN + CELL_WIDTH) * column, (CELL_MARGIN + CELL_HEIGHT) * row, CELL_WIDTH, CELL_HEIGHT]) 
                
                        #This code is used to display the number of neighbors each cell has
                #cell_pop = population_check(grid, row, column)
                #text = font.render(str(cell_pop), True, RED)
                #SCREEN.blit(text, ((CELL_MARGIN + CELL_WIDTH) * column, (CELL_MARGIN + CELL_HEIGHT) * row))
                   

                            
        #When paused i wanted it to be more responsive (faster)
        #When unpaused i did not want the cells to move too fast
        if PAUSED: 
            clock.tick(60)
        else:
            clock.tick(5)

        #update the display with all the changes
        pygame.display.update()
        

main()            
pygame.quit()    

        