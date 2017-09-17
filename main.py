import pygame
import time
import random
from units import Unit
from vectors import Vector

pygame.init()
game_title = 'Simple RTS'
width = 400
height = 400
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
GREEN = (0,255,0)
blue = (0,0,255)

gameDisplay = pygame.display.set_mode((width,height))
pygame.display.set_caption(game_title)
clock = pygame.time.Clock()

class Selection(object):
    '''Creates a selection box object'''
    def __init__(self,initial_position):
        self.initial_position = initial_position
        self.rect = None
        self.checked = False

    def update(self,select_rect):
        '''Recieves a rectangle and stores it as this selection objects rect'''
        self.rect = select_rect

    def draw(self,mouse_position,surface,color=GREEN,size=2):
        '''Draws the selection box on a given surface'''

        # Determine the min and max so that the x_len/y_len always draw correctly
        x1 = min(self.initial_position.x,mouse_position.x)
        y1 = min(self.initial_position.y,mouse_position.y)
        x2 = max(self.initial_position.x,mouse_position.x)
        y2 = max(self.initial_position.y,mouse_position.y)
        x_len = (x2 - x1)
        y_len = (y2 - y1)
        pygame.draw.rect(surface,color,[x1,y1,x_len,y_len],size)

        self.update((x1,y1,x2,y2))
        

soliders = [Unit(Vector(width/2,height/2)) for i in range(1)]

def game_loop():
    gameExit = False
    
    mouse_left_pressed = False
    selection_object   = None

    shift = False
    move_click = None
    
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Handles unit selection
                if event.button == 1:
                    mouse_left_pressed = True
                    selection_object   = Selection(Vector(event.pos[0],event.pos[1]))
                    for solider in soliders:
                        solider.selected = False
                        
                # Handles unit movement / attacking
                if event.button == 3:
                    move_click = Vector(event.pos[0],event.pos[1])
                    
            if event.type == pygame.MOUSEBUTTONUP:
                # Handles unit selection
                if event.button == 1:
                    mouse_left_pressed = False
                    selection_object.checked = True
                # Handles unit movement / attacking
                if event.button == 3:
                    move_click = None

            if event.type == pygame.KEYDOWN:
                # Handles movement / attacking queueing
                if event.key == pygame.K_RSHIFT or pygame.K_LSHIFT:
                    shift = True

            if event.type == pygame.KEYUP:
                # Handles movement / attacking queueing
                if event.key == pygame.K_RSHIFT or pygame.K_LSHIFT:
                    shift = False


    
        gameDisplay.fill(white)

        # Draws the selection box to the screen
        if mouse_left_pressed == True:
            mouse_pos = Vector(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
            selection_object.draw(mouse_pos,gameDisplay)

        # Checks the selection box against all units
        if selection_object != None:
            if selection_object.checked == False:
                for solider in soliders:
                    solider.check_selected(selection_object)
        
        # Renders soliders to screen and updates position
        for solider in soliders:
            solider.show(gameDisplay)
            solider.update()

            # Passes the soliders the mouse command if they are selected
            if solider.selected == True:
                if move_click != None:
                    solider.command_move(move_click,queue=shift)
    
        
        pygame.display.update()
        clock.tick(60)

game_loop()
pygame.quit() #stops pygame from running
quit() #quits python
