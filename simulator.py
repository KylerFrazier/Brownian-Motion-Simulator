from tkinter import Tk, Canvas, TclError, NW
from time import sleep
from random import random as rand

class BrownianSimulator:
    
    def __init__(self, particle_type, detector_orientation = "", 
                detector_size = 10, max_cycles = 1000, display = True, 
                w = 1280, h = 720, fps = 24, trace = False):
        
        self.display = display
        self.width = w
        self.height = h
        self.particle_type = particle_type
        self.frame_time = int(1000/fps)
        self.trace = trace
        self.collisions = 0
        self.cycle = 0
        self.max_cycles = max_cycles
        self.detector_size = detector_size

        if detector_orientation.lower() == "horizontal":
            self.detector_orientation = "Horizontal"
            self.detector_points = ((self.width/2 - 400 - self.detector_size/2, 
                                     self.height/2), 
                                    (self.width/2 - 400 + self.detector_size/2, 
                                     self.height/2))
        else:
            self.detector_orientation = "Vertical"
            self.detector_points = ((self.width/2 - 400, 
                                     self.height/2 - self.detector_size/2), 
                                    (self.width/2 - 400, 
                                     self.height/2 + self.detector_size/2))

        self.particles = {particle_type(self.width/2, self.height/2) : 0}

        if self.display:
            self.gui = Tk()
            self.gui.title("B R O W N I A N    M O T I O N    S I M U L A T O R")
            self.gui.geometry(f"{self.width}x{self.height}")
            self.canvas = Canvas(   self.gui, width = self.width, 
                                    height = self.height)
            self.canvas.configure(background='black')
            self.canvas.pack()
            self.canvas.create_line(*self.detector_points[0], 
                                    *self.detector_points[1], fill = "white")
            self.gui.after(0, self.animate)
            self.gui.mainloop()
        else:
            while self.animate():
                pass
    
    def result(self):
        
        return self.collisions

    def animate(self):
        
        if self.cycle > self.max_cycles:
            
            print()
            print("#========== Brownian Motion Simulator Results ==========#")
            print(f"Detector Orientation: {self.detector_orientation}")
            print(f"Total Number of Collisions: {self.collisions}")
            print("#=======================================================#")
            print()
            if self.display:
                self.gui.destroy()
            return False

        try:
            self.update()
        except TclError:
            exit(0)

        self.cycle += 1
        
        if self.display:
            self.gui.after(self.frame_time, self.animate)
        else:
            return True

    def update(self):
        
        if self.display and not self.trace:
            self.canvas.delete("animate")
        
        if rand() < self.particle_type.birth_chance:
            self.particles[self.particle_type(self.width/2, self.height/2)] = 0
        
        remove = set()

        for particle in self.particles:
            
            self.particles[particle] += 1
            particle.move()
            if self.display:
                particle.draw(self.canvas)
            
            if particle.check_line_collision(*self.detector_points):
                self.collisions += 1
                remove.add(particle)
            if self.particles[particle] > self.particle_type.life_time:
                remove.add(particle)
        
        for particle in remove:
            self.particles.pop(particle)
        
        if self.display:
            self.canvas.create_text(20, 20, text = f"Number of particles = {len(self.particles)}",
                                anchor = NW, tag = "animate", fill = "white")
            self.canvas.create_text(20, 50, text = f"Number of collisions = {self.collisions}", 
                                anchor = NW, tag = "animate", fill = "white")
