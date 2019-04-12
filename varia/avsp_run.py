from configparser import ConfigParser
from pathlib import Path
from sys import argv

import networkx as nx
import numpy as np

from randomize_grid import append_rand_edge

# read configuration for the simulation
avsp_config = ConfigParser()
avsp_config.read('avsp_config.ini')
default_run = 'default'  # must be defined in the config file!

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
except KeyError:
    print("[ERROR] Problem while reading section", run_name, "from the config file.")
    exit(1)

# prepare the output file
out_path = Path("avsp_results/" + run_name + ".npz")

# initialize array for the result
avsp_len = []

# initialize dict for saving
savez_dict = dict()

# repeat experiments
for trial in range(0, repeat_times):
    # construct the graph
    g = nx.grid_2d_graph(dim1, dim2)

    # calculate average shortest path
    avsp_len.append([])
    avsp_len[trial].append(nx.average_shortest_path_length(g))
    print("[INFO] Experiment:", trial, 'of', repeat_times, end='.\n')
    # repeat max_steps times
    for step in range(1, max_steps):
        g: nx.Graph = append_rand_edge(g)
        avsp_len[trial].append(nx.average_shortest_path_length(g))
    savez_dict['trial_' + str(trial)] = avsp_len[trial]

# save the results
np.savez(out_path, **savez_dict)
