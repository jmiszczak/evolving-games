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


import os
os.chdir(os.path.dirname(__file__))

import sys
sys.path.append("..")

from ParrondoGraphModel import ParrondoGraphModel
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

# size of the BA network
network_size = 20

# m param
m_param = 15

# graph used in the experiment
ba_graph = nx.generators.barabasi_albert_graph(network_size, m_param)

# each model has num_agents agents
num_agents = 2*network_size

# data from all simulations
wealth_data = []

# string with descriptions used in plots
plot_desc = 'game sequence: '+default_policy+', BAnet(' + str(network_size) +','+str(m_param) +')'

#%% simulaiton with fixed parameters

for _ in range(num_runs):
    # create a model
    model = ParrondoGraphModel(num_agents, ba_graph, init_wealth, default_policy, default_eps)

    # execute num_steps steps
    for _ in range(num_steps):
        model.step()
        
    for a in model.schedule.agents:
        wealth_data.append(a.wealth)


#%% wealth data for some agents
agent_wealth = model.datacollector.get_agent_vars_dataframe()
print(agent_wealth.head())

# one_agent_wealth = agent_wealth.xs(3, level="AgentID")
# agent_wealth.xs(1, level="AgentID").Wealth.plot(ylim=(0,1000))
for agn in range(num_agents):
    agent_wealth.xs(agn, level="AgentID").Wealth.plot(ylim=(0,500), title='Wealth for agents, ' + plot_desc )
        

#%% plot of the Gini index

data = model.datacollector.get_model_vars_dataframe()
gini_index_data = data.get('Gini index')

gini_plot=gini_index_data.plot(ylim=(0,1), title='Gini index, ' + plot_desc)
# print(gini_index_data.describe())
display(gini_plot)

# %% plot of the mean wealth

data = model.datacollector.get_model_vars_dataframe()
median_wealth_data=data.get('Median wealth')
median_wealth_data.plot(title='Median wealth, ' + plot_desc, ylim=(0,200))

print(median_wealth_data.describe())


# %%
fig = figure.Figure(figsize=(8,6))
axs = fig.add_subplot()
axs.hist(wealth_data, density=True, histtype='step', bins=int(num_runs/2))
axs.set_xlabel('Wealth')
display(fig)
