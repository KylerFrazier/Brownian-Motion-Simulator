from tkinter import Tk, Canvas, TclError, NW
from time import sleep
from random import random as rand
from math import inf, pi, sin, cos
from numpy.random import poisson
from brownians import ThermalNeutron

class BrownianSimulator:
    
    def __init__(self, particle_type = ThermalNeutron, max_cycles = 1000, 
        scale = 1, x0 = 0, y0 = 0, w0 = 0, h0 = 0, partitions = {10}, 
        detector_size = 0, detector_orientation = 0, det_x = 400, det_y = 0,
        display = True, w = 1280, h = 720, fps = 100, trace = False
    ):
        
        self.particle_type = particle_type
        self.scale = scale
        self.detector_size = detector_size
        self.partitions = sorted([
            (tup[0] + w/2, tup[1]) if hasattr(tup, "__len__") and len(tup) > 1 \
            else (inf, tup) for tup in partitions
        ])
        self.width = w
        self.height = h
        self.x0 = self.width/2 + x0
        self.y0 = self.height/2 - y0
        self.w0 = w0
        self.h0 = h0
        self.max_cycles = max_cycles
        self.display = display
        self.frame_time = int(1000/fps)
        self.trace = trace

        self.detector_orientation = detector_orientation
        det_angle = detector_orientation * pi / 180
        self.detector_points = ((
            self.width/2 + det_x + self.detector_size / 2 * cos(det_angle),
            self.height/2 - det_y - self.detector_size / 2 * sin(det_angle)), (
            self.width/2 + det_x - self.detector_size / 2 * cos(det_angle),
            self.height/2 - det_y + self.detector_size / 2 * sin(det_angle)
        ))
        
        self.collisions = 0
        self.cycle = 0

        self.particles = {particle_type(
            self.x0 + rand()*self.w0, 
            self.y0 + rand()*self.h0, 
            self.scale
        )}

        if self.display:
            
            self.gui = Tk()
            self.gui.title("B R O W N I A N    M O T I O N    S I M U L A T O R")
            self.gui.geometry(f"{self.width}x{self.height}")
            self.canvas = Canvas(
                self.gui, width = self.width, height = self.height
            )
            self.canvas.configure(background = "black")
            self.canvas.pack()
            self.canvas.create_line(
                *self.detector_points[0], *self.detector_points[1], 
                fill = "white"
            )
            self.canvas.create_rectangle(
                self.x0, self.y0, self.x0 + self.w0, self.y0 - self.h0,
                fill = "red4"
            )
            for x, _ in self.partitions:
                self.canvas.create_line(x, 0, x, self.height, fill = "gray")
            self.gui.after(0, self.animate)
            self.gui.mainloop()

        else:
            
            while self.animate(): 
                pass
    
    def result(self):
        
        return self.collisions

    def animate(self):
        
        if self.cycle > self.max_cycles:
            
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
        
        for _ in range(poisson(self.particle_type.birth_chance)):
            self.particles.add(self.particle_type(
                self.x0 + rand()*self.w0, 
                self.y0 - rand()*self.h0,
                self.scale
            ))
        
        remove = set()

        for particle in self.particles:
            
            particle.move(self.partitions)
            
            if self.display:
                particle.draw(self.canvas)
            
            if self.detector_size > 0 \
            and particle.check_line_collision(*self.detector_points):
                self.collisions += 1
                remove.add(particle)
            
            if particle.clock > particle.life_time:
                remove.add(particle)
        
        for particle in remove:
            self.particles.remove(particle)
        
        if self.display:
            
            self.canvas.create_text(
                20, 20, text = f"Number of particles = {len(self.particles)}",
                anchor = NW, tag = "animate", fill = "white"
            )
            
            if self.detector_size != 0:
                self.canvas.create_text(
                    20, 50, text = f"Number of collisions = {self.collisions}", 
                    anchor = NW, tag = "animate", fill = "white"
                )
