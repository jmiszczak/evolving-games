#!/usr/bin/env python
# coding: utf-8

#%% global packages
import mesa.batchrunner as mb
import numpy as np
import networkx as nx
import uuid
import pandas as pd

from IPython.core.display import display

import matplotlib as mpl
import matplotlib.figure as figure
mpl.rc('text', usetex = True)
mpl.rc('font', size = 10)


#%% local functions

script_path = ""

import os
try:
    script_path = os.path.dirname(__file__)
    os.chdir(script_path)
except FileNotFoundError:
    script_path = os.getcwd()
else:
    script_path = os.getcwd()

import sys
sys.path.append("..")

from JanosikGraphModel import JanosikGraphModel
import indicators

##############################################################################
############################## BATCH EXECUTION ###############################
##############################################################################

#%% simulation parameters for batch execution

# initial capital
init_wealth = 2

# bias in the Parronod scheme
default_eps = 0.005

# size of the grid
grid_width = 10
grid_height = 10

# graph used in the experiments
graph = nx.generators.lattice.grid_2d_graph(grid_width,grid_height,periodic=True)

graph_id = "w"+str(grid_width) + "_h"+str(grid_height)
graph_file_path = script_path + '/graphs/grid2d/' + graph_id + ".gz"
nx.readwrite.write_gexf(graph, graph_file_path)
# nx.draw(graph)


#%% batch execution of the simulations
#

fixed_params = {
        "graph_spec": graph_file_path,
        "init_wealth": init_wealth,
        "default_eps": default_eps,
        }

variable_params = { 
        "num_agents" : range(20, 121, 20),
        "default_policy" : ['A', 'B', 'AB', 'uniform'],
        "default_boost" : ["matthew", "antimatthew", "strongmatthew" ,"strongantimatthew"]
        }
         
batch_run = mb.BatchRunnerMP(
        JanosikGraphModel,
        nr_processes = 8,
        variable_parameters=variable_params,
        fixed_parameters=fixed_params,
        iterations=20,
        max_steps=500,
        model_reporters={
            "Gini index" : indicators.gini_index
            }
        )

exp_desc = 'janosik_'+"grid_"+str(grid_width)+'x'+str(grid_height)+"_"+str(batch_run.iterations)+"runs_"+str(batch_run.max_steps)+"steps_" + str(default_eps)
#%% run the experiment
print("[INFO] Executing", len(variable_params["num_agents"])*len(variable_params["default_policy"])*len(variable_params["default_boost"])*batch_run.iterations, "iterations.", flush=True)
batch_run.run_all()

#%% results form the batch execution
run_data =  batch_run.get_model_vars_dataframe()
# workaround for the Mesa bug
run_data.columns = ['num_agents', 'default_policy', 'default_boost', 'Run', 'Gini index', 'graph_spec', 'init_wealth', 'default_eps']

run_data.to_csv("data/"+exp_desc+".zip", index=False, compression=dict(method='zip', archive_name='data.csv'))