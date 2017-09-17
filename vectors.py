'''This file introduces the Vector class. This class will act like a mathematical
   vector
'''

import matplotlib.pyplot as plt

class Vector(object):

    def __init__(self,x,y,z=None):
        self.x = x
        self.y = y
        if z is not None:
            self.z = z
        else:
            self.z = None

    def get_direction_or_mag(self,magnitude=False):
        '''Returns the unit directional vector by computing magnitude and dividing
           components
        '''
        if self.z is not None:
            operand = (self.x)**2 + (self.y)**2 + (self.z)**2
            mag = (operand)**(0.5)
            unit_vector = Vector(self.x / mag, self.y / mag, self.z / mag)
        else:
            operand = (self.x)**2 + (self.y)**2
            mag = (operand)**(0.5)
            unit_vector = Vector(self.x / mag, self.y / mag)
            
        if magnitude:
            return mag
        else:
            return unit_vector

    def __add__(self,other):
        '''Returns the resultant vector of addition'''
        new_x = self.x + other.x
        new_y = self.y + other.y
        if self.z is not None:
            new_z = self.z + other.z
            return Vector(new_x, new_y, new_z)
        else:
            return Vector(new_x, new_y)

    def __sub__(self,other):
        '''Returns the resultant vector of subtraction'''
        negation = other.scale(-1)
        addition = self + negation
        return addition

    def __eq__(self,other):
        if other == None:
            return False
        if self.z is None:
            if self.x == other.x and self.y == other.y:
                return True
            else:
                return False
        else:
            if self.z == other.z and self.x == other.x and self.y == other.y:
                return True
            else:
                return False
        
    def scale(self,scalar):
        '''Returns a vector that has been multiplied by the scalar'''
        new_x = self.x * scalar
        new_y = self.y * scalar
        if self.z is not None:
            new_z = self.z * scalar
            return Vector(new_x, new_y, new_z)
        else:
            return Vector(new_x, new_y)

    def __str__(self):
        '''Prints a classic vector string representation: <x,y>'''
        if self.z is not None:
            return('<{},{},{}>'.format(str(self.x),str(self.y),str(self.z)))
        else:
            return('<{},{}>'.format(str(self.x),str(self.y)))

    def draw(self,origin=None):
        '''Draws the vector from the origin on a grid'''

        if self.z is not None:
            if origin is None:
                origin = Vector(0,0,0)
            x = origin.x, self.x
            y = origin.y, self.y
            z = origin.z, self.z
            plt.plot(x,y,z)
        else:
            if origin is None:
                origin = Vector(0,0)
            x = origin.x, self.x
            y = origin.y, self.y
            plt.plot(x,y)
        plt.show()


