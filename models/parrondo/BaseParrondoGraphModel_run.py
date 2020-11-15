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

from BaseParrondoGraphModel import BaseParrondoGraphModel
import indicators

#%%

##############################################################################
############################# SINGLE EXECUTION ###############################
##############################################################################

#%% simulation parameters

# initial capital
init_wealth = 100

# bias in the Parronod scheme
default_policy = 'AB'
default_eps = 0.002

# store data from num_runs
num_runs = 1

# each run has num_steps steps
num_steps = 100

# size of the grid
grid_width = 10
grid_height = 10

# each model has num_agents agents
num_agents = 10000

# data from all simulations
wealth_data = []
agent_counts = np.zeros((grid_width, grid_height))

# graph used in the experiments
graph = nx.generators.lattice.grid_2d_graph(grid_width,grid_height,periodic=True)

# string with descriptions used in plots
plot_desc = 'game sequence: '+default_policy+', grid=(' + str(grid_width) +','+str(grid_height) +')'

#%% simulation with fixed parameters

for _ in range(num_runs):
    # create a model
    model = BaseParrondoGraphModel(num_agents, graph, init_wealth, default_policy, default_eps)

    # execute num_steps steps
    for _ in range(num_steps):
        model.step()
        
    for a in model.schedule.agents:
        wealth_data.append(a.wealth)


#%% plot of the wealth data for agents
# agent_wealth = model.datacollector.get_agent_vars_dataframe()
# print(agent_wealth.head())

# one_agent_wealth = agent_wealth.xs(3, level="AgentID")
# agent_wealth.xs(1, level="AgentID").Wealth.plot(ylim=(0,1000))
# for agn in range(num_agents):
    # agent_wealth.xs(agn, level="AgentID").Wealth.plot(ylim=(50,150), title='Wealth for agents, ' + plot_desc )
        
#%% plots for selected indices

data = model.datacollector.get_model_vars_dataframe()
# median_wealth_data=data.get('Median wealth')
# median_wealth_data.plot(title='Median wealth, ' + plot_desc, ylim=(0,200))
# print(median_wealth_data.describe())

# mean_wealth_data=data.get('Mean wealth')
# mean_wealth_data.plot(title='Mean wealth, ' + plot_desc, ylim=(50,150))

# fig = figure.Figure(figsize=(8,6))

# #%%
fig = figure.Figure(figsize=(4,3))
axs = fig.add_subplot()
axs.set_ylim((98,102))
axs.plot(data['Mean wealth'])
axs.set_xlabel('step')
axs.set_title("policy: " + default_policy + ", agents: " + str(num_agents) +", bias: " + str(default_eps) )
display(fig)

# #%%
# for cell in model.grid.coord_iter():
#     cell_content, x, y = cell
#     agent_counts[x][y] = len(cell_content)    

# fig = mpl.figure.Figure(figsize=(8,8))
# axs = fig.add_subplot()

# axs.imshow(agent_counts, interpolation='none', cmap=mpl.cm.Greys)
# norm = mpl.cm.colors.Normalize(vmin=agent_counts.min(), vmax=agent_counts.max())
# fig.colorbar(mpl.cm.ScalarMappable(cmap=mpl.cm.Greys, norm=norm), ax=axs)

# display(fig)
