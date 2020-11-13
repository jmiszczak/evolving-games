#!/usr/bin/env python
# coding: utf-8

#%% global packages
import mesa.batchrunner as mb
# import numpy as np
import networkx as nx
import uuid
# import pandas as pd

from IPython.core.display import display

import matplotlib as mpl
# import matplotlib.figure as figure
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


# #%% wealth data for some agents
# agent_wealth = model.datacollector.get_agent_vars_dataframe()
# print(agent_wealth.head())

# # one_agent_wealth = agent_wealth.xs(3, level="AgentID")
# # agent_wealth.xs(1, level="AgentID").Wealth.plot(ylim=(0,1000))
# for agn in range(num_agents):
#     agent_wealth.xs(agn, level="AgentID").Wealth.plot(ylim=(0,500), title='Wealth for agents, ' + plot_desc )
        

#%% plot of the Gini index

data = model.datacollector.get_model_vars_dataframe()
gini_index_data = data.get('Gini index')

gini_plot=gini_index_data.plot(ylim=(0,1), title='Gini index, ' + plot_desc)
# print(gini_index_data.describe())
display(gini_plot)

#%% plot of the mean wealth

# data = model.datacollector.get_model_vars_dataframe()
# median_wealth_data=data.get('Median wealth')
# median_wealth_data.plot(title='Median wealth, ' + plot_desc, ylim=(0,200))

# print(median_wealth_data.describe())


#%%
# fig = figure.Figure(figsize=(8,6))
# axs = fig.add_subplot()
# axs.hist(wealth_data, density=True, histtype='step', bins=int(num_runs/2))
# axs.set_xlabel('Wealth')
# display(fig)


#%%
# for cell in model.grid.coord_iter():
#     cell_content, x, y = cell
#     agent_counts[x][y] = len(cell_content)    

# fig = mpl.figure.Figure(figsize=(8,8))
# axs = fig.add_subplot()

# axs.imshow(agent_counts, interpolation='none', cmap=mpl.cm.Greys)
# norm = mpl.cm.colors.Normalize(vmin=agent_counts.min(), vmax=agent_counts.max())
# fig.colorbar(mpl.cm.ScalarMappable(cmap=mpl.cm.Greys, norm=norm), ax=axs)

# display(fig)

##############################################################################
############################## BATCH EXECUTION ###############################
##############################################################################

#%% simulation parameters for batch execution

# initial capital
init_wealth = 2

# bias in the Parronod scheme
default_eps = 0.002

### graph used in the experiemnt
# size of the BA network
network_size = 100

# m param
m_param = 10

# graph used in the experiment
ba_graph = nx.generators.barabasi_albert_graph(network_size, m_param)
ba_graph_uuid = str(uuid.uuid4())
ba_graph_file_path = os.path.dirname(__file__) + '/graphs/ba/' + ba_graph_uuid + ".gz"
nx.readwrite.write_gexf(ba_graph, ba_graph_file_path)
nx.draw(ba_graph) 


#%% batch execution of the simulations
#

fixed_params = {
        "Gf": ba_graph_file_path,
        "init_wealth": init_wealth,
        "default_eps": default_eps
        }

variable_params = { 
        "N" : range(10, 101, 10),
        "default_policy" : ['A', 'B', 'AABB', 'uniform']
        }
         
batch_run = mb.BatchRunner(
        ParrondoGraphModel,
        variable_parameters=variable_params,
        fixed_parameters=fixed_params,
        iterations=50,
        max_steps=500,
        model_reporters={
            "Gini index" : indicators.gini_index
            }
        )

print("[INFO] Executing", len(variable_params["N"])*len(variable_params["default_policy"])*batch_run.iterations, "iterations.", flush=True)
batch_run.run_all()

#%% results form the batch execution

exp_desc = "graphBA("+str(network_size)+','+str(m_param)+")_"+str(batch_run.iterations)+"runs_"+str(batch_run.max_steps)+"steps"

#%%
run_data = batch_run.get_model_vars_dataframe()
run_data.head()

run_data.to_csv("data/"+exp_desc+".zip", index=False, compression=dict(method='zip', archive_name='data.csv'))


#%%
#run_data = pd.read_csv("data/"+exp_desc+".zip")

fig = mpl.figure.Figure(figsize=(8,8))
for i,curr_policy in enumerate(['A', 'B', 'AABB', 'uniform']):#= 'A'
# for i,curr_policy in enumerate(['A', 'uniform']):#= 'A'

    axs = fig.add_subplot(221+i)
    plot_desc = 'game sequence: '+curr_policy+", graphBA("+str(network_size)+','+str(m_param)+')'
    axs.scatter(run_data[(run_data.default_policy==curr_policy)].N,run_data[(run_data.default_policy==curr_policy)]['Gini index'],marker='x')
    #axs.set_xlabel('Number of agents')
    axs.set_xlim((9,101))
    axs.grid()
    axs.set_ylim((-0.01,1))
    # axs.set_ylabel('Gini index')
    axs.set_title(plot_desc)

display(fig)

fig.tight_layout()
fig.savefig("plots/"+ exp_desc +".pdf")
