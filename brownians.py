from random import random as rand
from math import cos, sin, pi, log as ln
from collisions import line_collision

class BrownianParticle:

    def __init__(self, x0, y0, r, d, color):
        
        self.x = x0             # starting x
        self.y = y0             # starting y
        self.x2 = x0            # next x
        self.y2 = y0            # next y
        self.r = r              # radius
        self.d = d              # average distance traveled
        self.color = color      # display color
    
    def move(self):
        
        self.x = self.x2
        self.y = self.y2

        dist = -self.d * ln(1 - rand())
        theta = 2 * pi * rand()

        self.x2 = self.x + dist * cos(theta)
        self.y2 = self.y + dist * sin(theta)
    
    def check_line_collision(self, p1, p2):
        return line_collision(p1, p2, (self.x, self.y), (self.x2, self.y2))

    def draw(self, canvas):
        
        canvas.create_line(self.x, self.y, self.x2, self.y2,
                                fill = self.color, tag = "animate")
        canvas.create_oval(self.x - self.r, self.y - self.r, 
                                self.x + self.r, self.y + self.r, 
                                fill = self.color, tag = "animate")

class ThermalNeutron(BrownianParticle):
    
    life_time = 1000
    birth_chance = 100/life_time
    avg_step_size = 10

    def __init__(self, x0, y0):
        
        BrownianParticle.__init__(  self, x0, y0, 2, 
                                    ThermalNeutron.avg_step_size, "white")
        