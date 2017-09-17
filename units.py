'''This module allows you to create units of circle and square type
   that have the same functionality. They can be commanded to attack
   and defend.
'''
import pygame
from vectors import Vector
import math

RED   = (255,0,0)
BLUE  = (0,0,255)
GREEN = (0,255,0)

class Unit(object):
    
    def __init__(self,position,team=RED):
        self.position = position
        self.velocity = Vector(0,0)
        self.color    = team
        self.selected = False 

        # Relevant to command_move method
        self.move_list = []
        self.distance_from_target = 0
        self.target_reached = True

        # Relevant to the command_attack method
        self.attacking = False
        self.target_enemy = 0  # not really sure what to put here

    def update(self,accuracy=10,speed=5):
        '''If we have not reached the target and there are moves in the queue, move to target
           and shorten the queue. If we have reached the target and there is only 1 item in
           the que, stop moving.
        '''
        
        if self.target_reached == False:
            distance_vector = self.move_list[0] - self.position
            distance        = distance_vector.get_direction_or_mag(magnitude=True)
            if distance <= accuracy and len(self.move_list) == 1:
                self.target_reached = True
                self.move_list[0] = self.position
                self.velocity = Vector(0,0)
            if distance <= accuracy and len(self.move_list) > 1:
                self.move_list.pop(0)

        # Draws a unit directional vector from this unit to the mouse position
        # Then scales that by the speed it will travel to the desired location
        if self.target_reached == False:
            pointer_vector      = self.move_list[0] - self.position
            unit_pointer_vector = pointer_vector.get_direction_or_mag()
            move_vector         = unit_pointer_vector.scale(speed)
            self.velocity       = move_vector
            
        self.position += self.velocity

    def command_move(self,mouse_vector,queue=False):
        '''If the queue parameter is True, it will store the mouse_vector in a list.
           Expected: mouse_position as a Vector()
        '''

        # if i pass as a tuple (action_type,action_parameter) I can queue up
        # move actions and attack actions by having an execute_action() method
        # this method would know wether to call command_move() or command_attack()
        # based on the action_type
        
        if queue and self.move_list[0] == self.position:
            # this will introduce a bug potentionally
            self.move_list = []
            self.target_reached = False
            self.move_list.append(mouse_vector)
        elif queue:
            self.move_list.append(mouse_vector)
        else:
            self.move_list = []
            self.target_reached  = False
            self.move_list.append(mouse_vector)

    def commad_attack(self):
        pass

    def check_target_dead(self):
        pass

    def check_selected(self,selection_object):
        '''Receives a selection object and determines if the units position falls within
            the selection square to mark this unit as selected.
        '''
        
        if selection_object != None:
            if self.position.x >= selection_object.rect[0] and self.position.x <= selection_object.rect[2]:
                if self.position.y >= selection_object.rect[1] and self.position.y <= selection_object.rect[3]:
                    self.selected = True

    def show(self,surface,size=8,selection_offset=5,selection_width=1):
        '''Draws the unit to screen. The offset parameter determines how much larger
            the selection circle is around the unit.
        '''
        
        pygame.draw.ellipse(surface,self.color,[self.position.x,self.position.y,size,size])
        if self.selected == True:
            off_set = selection_offset * math.sin(math.radians(45))
            new_x,new_y = self.position.x - off_set, self.position.y - off_set
            new_r = size + off_set * 2
            pygame.draw.ellipse(surface,GREEN,[new_x,new_y,new_r,new_r],selection_width)
