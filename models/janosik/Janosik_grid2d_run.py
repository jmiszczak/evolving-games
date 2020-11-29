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
mpl.rc('font', size = 12)


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
############################## SINGLE EXECUTION ###############################
##############################################################################

#%% simulation parameters for batch execution

# initial capital
init_capital = 10

# size of the grid
grid_width = 10
grid_height = 10

# graph used in the experiments
graph_id = "w"+str(grid_width) + "_h"+str(grid_height)
graph_file_path = script_path + '/graphs/grid2d/' + graph_id + ".gz"

# graph generation and saving - ca be used only onece for the grid
# graph = nx.generators.lattice.grid_2d_graph(grid_width,grid_height,periodic=True)
# nx.readwrite.write_gexf(graph, graph_file_path)
# nx.draw(graph)

# value of the bias used in the experiments
default_eps = 0.15
num_agents = 2
default_boost = "matthew"

#%% simulaiton with fixed parameters
num_steps = 1000
capital_data = []

# create a model
model = JanosikGraphModel(num_agents, graph_file_path, init_capital, default_eps, default_boost)

# execute num_steps steps
for _ in range(num_steps):
    model.step()
    
for a in model.schedule.agents:
    capital_data.append(a.capital)


#%% wealth data for some agents
agent_capital = model.datacollector.get_agent_vars_dataframe()
print(agent_capital.head())

# one_agent_wealth = agent_wealth.xs(3, level="AgentID")
# agent_wealth.xs(1, level="AgentID").Wealth.plot(ylim=(0,1000))
for agn in range(num_agents):
    agent_capital.xs(agn, level="AgentID").Capital.plot(ylim=(-1,20), title='Capital for agents')
        

#%% plot of the Gini index

data = model.datacollector.get_model_vars_dataframe()
gini_index_data = data.get('Gini index')
total_capital_data = data.get('Total capital')

fig = mpl.figure.Figure(figsize=(4,3))
axs = fig.add_subplot()
axs.plot(gini_index_data)
axs.set_title('Gini index')
display(fig)


fig = mpl.figure.Figure(figsize=(4,3))
axs = fig.add_subplot()
axs.plot(total_capital_data)
axs.set_title('Total capital for agents')
display(fig)
