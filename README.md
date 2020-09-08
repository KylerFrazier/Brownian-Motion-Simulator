# **Brownian Motion Simulator**
## Author: Kyler Frazier

## Description
This repository contains a 2D simulator for Brownian motion of particles, written in Python. It allows the user to visualize the process with an animation, has the option of adding a 1D detector, and can gather/record data of different simulations.

## Prerequisites
- Python: The project will work with any version of Python 3.x, though it may also work with some versions of Python 2.x (though I have not checked myself).
- NumPy - Python library: Install with pip as follows.  
`$ python -m pip install numpy`
- matlibplot - Python library: Install with pip as follows.  
`$ python -m pip install matlibplot`

## Running
Navigate to the project directory (which should include all of the files in this repository) and run the following line.  
`$ python main.py`

## Parameters
There are a handful of parameters that will affect how the simulation runs. The majority of these parameters are set in `main.py`, and the user should open the file and add them manually (see `main.py` for examples).
- `name`: The name of a batch of trials.
- `trials`: The number of trials to run with a set of parameters.
- `particle_type`: The particle type to be run with a set of trials.
- `scale`: The scale of the size of the environment by pixel side length.
- `x0`, `y0`: The spawning position of the particles in cartesian coordinates. The point `(0,0)` represents the center of the screen.
- `w0`, `h0`: The width and height of a box which originates at `(x0, y0)`. Particles will be able to spawn in the area of this box.
- `detector_size`: The length of the detector. Set this value to `0` to remove the detector.
- `detector_orientation`: The angle of the detector in degrees.
- `det_x`, `det_y`: The center position of the detector. 
- `partitions`: The x-coordinate of the right most edge of horizontal partitions of the simulated world and the particle speeds within each of them. Inputed as a set of tuples: `{(x1, speed1), (x2, speed2), speed3}`. Note that the last partition did not need an x-coordinate because the x-coordinate of the right most position is at positive infinity. 
- `max_cycles`: The number of "frames" in a simulation.
- `display`: A boolean which determines whether or not to display an animation.
- `w`, `h`: The width and height of a screen's dimensions.
- `fps`: The frame rate of an animation in frames per second.
- `trace`: A boolean which determines whether or not to trace the paths of each particle in an animation.
Different types of particles can be edited in `brownians.py`. Each type of particle has a set of parameters which can be edited.
- `life_time`: The number of frames that the neutron stays alive for.
- `birth_chance`: The probability of a particle being born in a "frame".

## Output
If there was a detector in at least one simulation for a batch of trials, an output will be created in the `output` directory. Each output consists of an image of a histogram of the set of trials as well as a text file which contains the raw detection data and a list of parameters for the trial

## Animation
One pixel in the animation corresponds to one square centimeter. The flow of time in the animation is not reflective of the real world; it is only determined by the user inputed `fps` parameter. 