from random import random as rand
from math import cos, sin, tan, pi, log as ln
from collisions import line_collision
from numpy.random import poisson, exponential

MAX_PARTICLES_ON_SCREEN = 100

N_A = 6.0221409 * 10**23 # (molecules per mole) Avogadro's number
BARN = 10**-24 # (cm^2) Cross sectional area approximation

class BrownianParticle(object):

    avg_life_time = 1000 # Average number of frames before the particle dies
    birth_chance = MAX_PARTICLES_ON_SCREEN/avg_life_time # Average number of new particles per frame
    cross_sectional_area = BARN

    def __init__(self, x0, y0, r, color, scale = 1):
        
        self.x = x0             # starting x
        self.y = y0             # starting y
        self.x2 = x0            # next x
        self.y2 = y0            # next y
        self.r = r              # radius
        self.color = color      # display color
        
        self.clock = 0
        self.life_time = poisson(self.avg_life_time)

        # Mean Free Path scalar factor
        self.k = 1 / (N_A * self.cross_sectional_area * scale)
    
    def get_partition(self, partitions) -> int:

        i = 0
        for x, medium in partitions:
            if self.x2 < x:
                return i, medium
            i += 1
        assert False, "Particle's destination was not in space."

    def move(self, partitions):

        self.x = self.x2
        self.y = self.y2

        x_prime = self.x
        y_prime = self.y

        theta = 2 * pi * rand()

        p1, medium = self.get_partition(partitions)
        while True:
            
            step = exponential(self.k * medium.molecular_mass / medium.density)
            self.x2 = x_prime + step * cos(theta)
            self.y2 = y_prime + step * sin(theta)

            p2, _ = self.get_partition(partitions)

            if p1 == p2: 
                break
            else:
                if p2 > p1:
                    x_prime = partitions[p1][0]
                    p1 += 1
                else:
                    p1 -= 1
                    x_prime = partitions[p1][0]
                y_prime = (x_prime - self.x) * tan(theta) + self.y
                medium = partitions[p1][1]

        self.clock += 1
    
    def check_line_collision(self, p1, p2):
        
        return line_collision(p1, p2, (self.x, self.y), (self.x2, self.y2))

    def draw(self, canvas):
        
        canvas.create_line(
            self.x, self.y, self.x2, self.y2,
            fill = self.color, tag = "animate"
        )
        canvas.create_oval(
            self.x - self.r, self.y - self.r, 
            self.x + self.r, self.y + self.r,
            fill = self.color, tag = "animate"
        )

class ThermalNeutron(BrownianParticle):
    
    avg_life_time = 500
    birth_chance = 100/avg_life_time
    cross_sectional_area = BARN

    def __init__(self, x0, y0, scale = 1):
        
        super().__init__(x0, y0, 2, "white", scale)
        