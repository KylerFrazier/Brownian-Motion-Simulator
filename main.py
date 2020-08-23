from simulator import BrownianSimulator
from brownians import ThermalNeutron
from save_data import save_hv_data

if __name__ == "__main__":
    
    # Parameters
    
    trials = 1
    particle_type = ThermalNeutron
    detector_size = 10
    max_cycles = 10000
    display = False
    fps = 100

    # Simulating and getting data

    h = []
    for i in range(1, trials+1):
        sim = BrownianSimulator(particle_type = particle_type,
                                detector_orientation = "horizontal",
                                detector_size = detector_size,
                                max_cycles = max_cycles, 
                                display = display, 
                                fps = fps)
        h.append(sim.result()) 
        print(f"Progress: {50*i/trials}%")
    
    v = []
    for i in range(1, trials+1):
        sim = BrownianSimulator(particle_type = particle_type,
                                detector_orientation = "vertical",
                                detector_size = detector_size,
                                max_cycles = max_cycles, 
                                display = display, 
                                fps = fps)
        v.append(sim.result())
        print(f"Progress: {50+50*i/trials}%")
    
    print()
    print(f"Horizontal Detector Summary:\n{h}")
    print(f"Vertical Detector Summary:\n{v}")
    print()
    
    # Processing and saving data

    save_hv_data(h, v, detector_size, particle_type, trials, max_cycles)
