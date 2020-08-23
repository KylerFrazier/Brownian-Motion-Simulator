from numpy import array, linspace
from matplotlib import pyplot
import os

def save_hv_data(h, v, detector_size, particle_type, trials, max_cycles):
    
    # Processing Data

    a = array(h)
    b = array(v)
    max_total = max(max(h),max(v)) + 1
    min_total = min(min(h),min(v))
    num_bins = max_total - min_total + 1
    bins = linspace(min_total, max_total, num_bins)
    pyplot.hist(a, bins, alpha=0.5, label="Horizontal")
    pyplot.hist(b, bins, alpha=0.5, label="Vertical")
    pyplot.legend(loc="upper right")

    # Saving data

    folder = os.path.join('.', f"output_detectorSize-{detector_size}_avgStep-{particle_type.avg_step_size}_lifeTime-{particle_type.life_time}")
    if not os.path.exists(folder):
        os.mkdir(folder)
    
    i = 1
    while os.path.exists(f"{folder}/trials-{trials}_cycles-{max_cycles}_({i}).txt"):
        i += 1
    pyplot.savefig(f"{folder}/trials-{trials}_cycles-{max_cycles}_({i}).png")
    with open(f"{folder}/trials-{trials}_cycles-{max_cycles}_({i}).txt", "w") as output:
        output.write(f"Detector Size: {str(detector_size)}, Particle Type: {particle_type.__name__}, Trials: {trials}, Max Cycles: {max_cycles}\n")
        output.write("Horizontal Detector:\n")
        output.write(str(h).strip("[]"))
        output.write("\nVertical Detector:\n")
        output.write(str(v).strip("[]"))
    pyplot.show()