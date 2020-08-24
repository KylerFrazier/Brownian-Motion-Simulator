import os
from numpy import array, linspace
from matplotlib import pyplot
from datetime import datetime

def save_sim_data(params_list, results, trials):
    
    # Processing Data

    max_total = max(i for result in results.values() for i in result) + 1
    min_total = min(i for result in results.values() for i in result)
    num_bins = max_total - min_total + 1

    bins = linspace(min_total, max_total, num_bins)
    for name, result in results.items():
        pyplot.hist(array(result), bins, alpha = 0.5, label = name)
    pyplot.legend(loc = "upper right")

    # Saving data

    folder = os.path.join('.', "output")
    if not os.path.exists(folder):
        os.mkdir(folder)
    
    datetime_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    file_name = f"{folder}/datetime-{datetime_str}_trials-{trials}"
    if os.path.exists(f"{file_name}.png"):
        i = 1
        while os.path.exists(f"{file_name}_({i}).png"):
            i += 1
        file_name += f"_({i})"
    
    pyplot.savefig(f"{file_name}.png")
    
    with open(f"{file_name}.txt", "w") as output:
        for params in params_list:
            name = params.pop("name")
            result = results[name]
            output.write(f"{name}\nresults : {str(result).strip('[]')}\n")
            for param_name, param in sorted(params.items()):
                output.write(f"{param_name} : {str(param)}\n")
            output.write('\n')
    
    pyplot.show()