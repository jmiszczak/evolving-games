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

from JanosikParrondoGraphModel import JanosikParrondoGraphModel

##############################################################################
############################# SINGLE EXECUTION ###############################
##############################################################################


#%% simulation parameters for batch execution

# initial capital
init_capital = 20

# size of the grid
grid_width = 10
grid_height = 10

# graph used in the experiments
graph_id = "w"+str(grid_width) + "_h"+str(grid_height)
graph_file_path = script_path + '/graphs/grid2d/' + graph_id + ".gz"

# graph generation and saving - can be used only onece for the grid
# graph = nx.generators.lattice.grid_2d_graph(grid_width,grid_height,periodic=True)
# nx.readwrite.write_gexf(graph, graph_file_path)
# nx.draw(graph)

# bias in the Parronod scheme, policy, number of agents
default_policy = 'B'
default_eps = 0.01
default_boost = "matthew"
num_agents = 300

# string with descriptions used in plots
plot_desc = 'game sequence: '+default_policy+', grid=(' + str(grid_width) +','+str(grid_height) +')'


#%% simulaiton with fixed parameters
num_steps = 300
capital_data = []

# create a model
model = JanosikParrondoGraphModel(num_agents, graph_file_path, init_capital, default_policy, default_eps, default_boost)

# execute num_steps steps
for _ in range(num_steps):
    model.step()
    
for a in model.schedule.agents:
    capital_data.append(a.capital)


#%% plot of the wealth data for agents
# agent_wealth = model.datacollector.get_agent_vars_dataframe()
# print(agent_wealth.head())

# # one_agent_wealth = agent_wealth.xs(3, level="AgentID")
# # agent_wealth.xs(1, level="AgentID").Wealth.plot(ylim=(0,1000))
# for agn in range(num_agents):
#     agent_wealth.xs(agn, level="AgentID").Capital.plot(ylim=(0,50), title='Wealth for agents, ' + plot_desc )
        

#%% plot of the Gini index

data = model.datacollector.get_model_vars_dataframe()
gini_index_data = data.get('Gini index')

gini_plot=gini_index_data.plot(ylim=(0,0.5), title='Gini index, ' + plot_desc)
print(gini_index_data.describe())
# display(gini_plot)

# #%% plot of the mean wealth

# min_capital_data = data.get('Min capital')
# max_capital_data = data.get('Max capital')

# min_capital_plot=min_capital_data.plot(ylim=(-100,100), title='Min capital, ' + plot_desc)
# max_capital_plot=max_capital_data.plot(ylim=(-100,100), title='Max capital, ' + plot_desc)
# print(gini_index_data.describe())
# display(mean_capital_plot)

# data = model.datacollector.get_model_vars_dataframe()
# mean_capital_data=data.get('Mean capital')
# mean_capital_data.plot(title='Mean capital, ' + plot_desc, ylim=(0,200))

# print(median_wealth_data.describe())

#%%
fig = figure.Figure(figsize=(8,6))
axs = fig.add_subplot()
axs.hist(capital_data, density=True, histtype='step')#, bins=int(num_agents/2))
axs.set_xlabel('Capital')
display(fig)


