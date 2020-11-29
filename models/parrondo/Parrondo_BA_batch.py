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

from ParrondoGraphModel import ParrondoGraphModel
import indicators



##############################################################################
############################## BATCH EXECUTION ###############################
##############################################################################

#%% simulation parameters for batch execution

# initial capital
init_wealth = 10

# bias in the Parronod scheme
default_eps = 0.005

### graph used in the experiemnt
# size of the BA network
network_size = 100

# m param
m_param = 10

# graph used in the experiment
ba_graph = nx.generators.barabasi_albert_graph(network_size, m_param)
ba_graph_uuid = str(uuid.uuid4())
ba_graph_file_path = script_path + '/graphs/ba/' + ba_graph_uuid + ".gz"
nx.readwrite.write_gexf(ba_graph, ba_graph_file_path)
# nx.draw(ba_graph) 


#%% batch execution of the simulations
#

fixed_params = {
        "graph_spec": ba_graph_file_path,
        "init_wealth": init_wealth,
        "default_eps": default_eps,
        }

variable_params = { 
        "num_agents" : range(10, 101, 10),
        "default_policy" : ['A', 'B', 'AB', 'uniform'],
        "default_boost" : ["matthew", "antimatthew", "strongmatthew" ,"strongantimatthew"]
        }
         
batch_run = mb.BatchRunnerMP(
        ParrondoGraphModel,
        nr_processes = 8,
        variable_parameters=variable_params,
        fixed_parameters=fixed_params,
        iterations=10,
        max_steps=500,
        model_reporters={
            "Gini index" : indicators.gini_index
            }
        )

exp_desc = "graphBA("+str(network_size)+','+str(m_param)+")_"+str(batch_run.iterations)+"runs_"+str(batch_run.max_steps)+"steps_" + str(default_eps)
#%% run the experiment
print("[INFO] Executing", len(variable_params["num_agents"])*len(variable_params["default_policy"])*len(variable_params["default_boost"])*batch_run.iterations, "iterations.", flush=True)
batch_run.run_all()

#%% results form the batch execution
run_data =  batch_run.get_model_vars_dataframe()
# workaround for the Mesa bug
run_data.columns = ['num_agents', 'default_policy', 'default_boost', 'Run', 'Gini index', 'graph_spec', 'init_wealth', 'default_eps']

run_data.to_csv("data/"+exp_desc+".zip", index=False, compression=dict(method='zip', archive_name='data.csv'))

#%% read data from file
run_data = pd.read_csv(script_path + "/data/"+exp_desc+".zip")
gini_data = np.loadtxt(script_path+"/data/gini_index_values.dat")

# %% plot data
fig = mpl.figure.Figure(figsize=(8,8))
for i,curr_policy in enumerate(['A', 'B', 'AB', 'uniform']):

    axs = fig.add_subplot(221+i)
    plot_desc = 'game: '+curr_policy+", BA("+str(network_size)+','+str(m_param)+')'
    axs.grid(alpha=0.5,ls='--')
    
    axs.scatter(run_data[(run_data.default_policy==curr_policy) & (run_data.default_boost == 'matthew')].num_agents, 
                run_data[(run_data.default_policy==curr_policy) & (run_data.default_boost == 'matthew')]['Gini index'],
                marker='x',color='r',s=1)
    
    axs.scatter(run_data[(run_data.default_policy==curr_policy) & (run_data.default_boost == 'strongmatthew')].num_agents, 
                run_data[(run_data.default_policy==curr_policy) & (run_data.default_boost == 'strongmatthew')]['Gini index'],
                marker='x',color='b')
    
    axs.scatter(run_data[(run_data.default_policy==curr_policy) & (run_data.default_boost == 'antimatthew')].num_agents, 
                run_data[(run_data.default_policy==curr_policy) & (run_data.default_boost == 'antimatthew')]['Gini index'],
                marker='o',color='g')
    
    axs.scatter(run_data[(run_data.default_policy==curr_policy) & (run_data.default_boost == 'strongantimatthew')].num_agents, 
                run_data[(run_data.default_policy==curr_policy) & (run_data.default_boost == 'strongantimatthew')]['Gini index'],
                marker='+',color='k')
    
    axs.plot(gini_data,"k:")
    #axs.set_xlabel('Number of agents')
    axs.set_xlim((0,101))
    axs.set_ylim((-0.01,0.5))
    # axs.set_ylabel('Gini index')
    axs.set_title(plot_desc)

display(fig)

fig.tight_layout()
fig.savefig("plots/"+ exp_desc +".pdf")
