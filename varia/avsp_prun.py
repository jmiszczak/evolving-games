from configparser import ConfigParser
from multiprocessing import Process, Manager
from pathlib import Path
from sys import argv

import networkx as nx
import numpy as np

from randomize_grid import append_rand_edge

# read configuration for the simulation
avsp_config = ConfigParser()
avsp_config.read('avsp_config.ini')
default_run = 'defaultp'  # must be defined in the config file!

# read the name of the config section to be used in the current run
try:
    run_name = argv[1]
except:
    run_name = default_run
    print("[WARNING] Specify the name of the run (section in *.ini file)!")
    print("[WARNING] Using run '", run_name, "'.", sep="")

# read simulation parameters for the current run
try:
    dim1 = int(avsp_config[run_name]['dim1'])
    dim2 = int(avsp_config[run_name]['dim2'])
    max_steps = int(avsp_config[run_name]['max_steps'])
    repeat_times = int(avsp_config[run_name]['repeat_times'])
    workers_num = int(avsp_config[run_name]['workers_num'])
except KeyError:
    print("[ERROR] Problem while reading section", run_name, "from the config file.")
    exit(1)

# prepare the output file
out_path = Path("avsp_results/" + run_name + ".npz")


# define the experiment
def experiment(trial, avsp_len):
    # construct the graph
    g = nx.grid_2d_graph(dim1, dim2)

    # calculate average shortest path
    avsp_len[trial].append(nx.average_shortest_path_length(g))
    print("[INFO] Experiment:", trial, end='')
    # repeat max_steps times
    for step in range(1, max_steps):
        g: nx.Graph = append_rand_edge(g)
        avsp_len[trial].append(nx.average_shortest_path_length(g))
    # print(avsp_len[trial])
    print(".", sep='', end='\n')


# execute in parallel
manager = Manager()

# initialize array for the result
avsp_len = manager.list()

# initialize dict for saving
savez_dict = dict()

# prepare storage for each process from the pool
for trial in range(0, repeat_times):
    avsp_len.append(manager.list())

# prepare the pull of processes
process = []
for trial in range(0, repeat_times):
    process.append(Process(target=experiment, args=(trial, avsp_len)))

# dispatch the tasks
for trial in range(0, repeat_times, workers_num):
    # distribute among the workers
    for p_num in range(0, workers_num):
        process[p_num + trial].start()

    # joint the results
    for p_num in range(0, workers_num):
        process[trial + p_num].join()

# prepare the dict for saving
for trial in range(0, repeat_times):
    savez_dict['trial_' + str(trial)] = list(avsp_len[trial])

# save the results
np.savez(out_path, **savez_dict)
