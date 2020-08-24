from math import inf
from simulator import BrownianSimulator
from brownians import ThermalNeutron
from save_data import save_sim_data

if __name__ == "__main__":
    
    # Parameters
    
    params_list = []

    # params_list.append({
    #     "name": "Horizontal Detector",
    #     "trials": 100,
    #     "particle_type": ThermalNeutron,
    #     "x0": 0, "y0": 0,
    #     "w0": 0, "h0": 0,
    #     "detector_size": 20,
    #     "detector_orientation": 0,
    #     "det_x": -300, "det_y": -200,
    #     "partitions": {39277},
    #     "max_cycles": 1000,
    #     "display": False
    # })
    # params_list.append({
    #     "name": "Vertical Detector",
    #     "trials": 100,
    #     "particle_type": ThermalNeutron,
    #     "x0": 0, "y0": 0,
    #     "w0": 0, "h0": 0,
    #     "detector_size": 20,
    #     "detector_orientation": 90,
    #     "det_x": -300, "det_y": -200,
    #     "partitions": {39277},
    #     "max_cycles": 1000,
    #     "display": False
    # })

    params_list.append({
        "name": "Starting in Fuel",
        "trials": 1,
        "particle_type": ThermalNeutron,
        "x0": 60, "y0": -700/2,
        "w0": 80, "h0": 700,
        "detector_size": 10,
        "partitions": {(-50, 39277), (50, 16.6), 8.627},
        "max_cycles": 1000,
        "display": True,
        "w": 1280, "h": 720,
        "fps": 100,
        "trace": False
    })
    params_list.append({
        "name": "Starting in Metal",
        "trials": 1,
        "particle_type": ThermalNeutron,
        "x0": -40, "y0": -700/2,
        "w0": 80, "h0": 700,
        "detector_size": 10,
        "partitions": {(-50, 39277), (50, 16.6), 8.627},
        "max_cycles": 1000,
        "display": True,
        "w": 1280, "h": 720,
        "fps": 100,
        "trace": False
    })

    # Simulating and getting data

    total_trials = sum(params["trials"] for params in params_list)
    results = {}

    progress = 0.0
    print(f"\nProgress: {progress}%")

    for params in params_list:

        name = params.pop("name")
        trials = params.pop("trials")
        result = []
        
        for i in range(1, trials + 1):
            
            sim = BrownianSimulator(**params)
            result.append(sim.result())
            print(f"Progress: {progress + 100*i/total_trials}%")
        
        progress += 100*i/total_trials

        print(f"\n#========== {name} ==========#")
        print(result)
        print(f"#{'='*(22+len(name))}#\n")
        if "detector_size" in params and params["detector_size"] != 0:
            results[name] = result
        params["name"] = name
        params["trials"] = trials
    
    # Process and save data as needed

    params_with_data = []
    for params in params_list:
        if "detector_size" in params and params["detector_size"] != 0:
            params_with_data.append(params)
        else:
            total_trials -= params["trials"]
    if len(params_with_data) != 0:
        save_sim_data(params_with_data, results, total_trials)

