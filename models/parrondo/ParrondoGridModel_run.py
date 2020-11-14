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
#os.chdir(os.path.dirname(__file__))

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
default_policy = 'A'
default_eps = 0.002

# store data from num_runs
num_runs = 1

# each run has num_steps steps
num_steps = 100

# size of the grid
grid_width = 10
grid_height = 10

# each model has num_agents agents
num_agents = 2*grid_width*grid_height

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
    model = ParrondoGraphModel(num_agents, graph, init_wealth, default_policy, default_eps)

    # execute num_steps steps
    for _ in range(num_steps):
        model.step()
        
    for a in model.schedule.agents:
        wealth_data.append(a.wealth)


#%% plot of the wealth data for agents
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

#%% plot of the mean wealth

data = model.datacollector.get_model_vars_dataframe()
median_wealth_data=data.get('Median wealth')
median_wealth_data.plot(title='Median wealth, ' + plot_desc, ylim=(0,200))

print(median_wealth_data.describe())

#%%
fig = figure.Figure(figsize=(8,6))
axs = fig.add_subplot()
axs.hist(wealth_data, density=True, histtype='step', bins=int(num_runs/2))
axs.set_xlabel('Wealth')
display(fig)

#%%
for cell in model.grid.coord_iter():
    cell_content, x, y = cell
    agent_counts[x][y] = len(cell_content)    

fig = mpl.figure.Figure(figsize=(8,8))
axs = fig.add_subplot()

axs.imshow(agent_counts, interpolation='none', cmap=mpl.cm.Greys)
norm = mpl.cm.colors.Normalize(vmin=agent_counts.min(), vmax=agent_counts.max())
fig.colorbar(mpl.cm.ScalarMappable(cmap=mpl.cm.Greys, norm=norm), ax=axs)

display(fig)

##############################################################################
############################## BATCH EXECUTION ###############################
##############################################################################

#%% simulation parameters for batch execution

# initial capital
init_wealth = 2

# bias in the Parronod scheme
default_eps = 0.002

# size of the grid
grid_width = 10
grid_height = 10


# graph used in the experiments
graph = nx.generators.lattice.grid_2d_graph(grid_width,grid_height,periodic=True)

graph_id = "w"+str(grid_width) + "_h"+str(grid_height)
graph_file_path = os.path.dirname(__file__) + './graphs/grid2d/' + graph_id + ".gz"
nx.readwrite.write_gexf(graph, graph_file_path)
nx.draw(graph)


#%% batch execution of the simulations

fixed_params = {
        "init_wealth": init_wealth,
        "default_eps": default_eps,
        "Gf": graph_file_path
        }

variable_params = { 
        "N" : range(10, 101, 10),
        "default_policy" : ['A', 'B', 'AB', 'uniform']
        }
         
batch_run = mb.BatchRunner(
        ParrondoGraphModel,
        variable_parameters=variable_params,
        fixed_parameters=fixed_params,
        iterations=1,
        max_steps=100,
        model_reporters={
            "Gini index" : indicators.gini_index
            }
        )

exp_desc = "grid_"+str(grid_width)+'x'+str(grid_height)+"_"+str(batch_run.iterations)+"runs_"+str(batch_run.max_steps)+"steps"


#%% run the experiment
print("[INFO] Executing", len(variable_params["N"])*len(variable_params["default_policy"])*batch_run.iterations, "iterations.", flush=True)
batch_run.run_all()

#%% results form the batch execution
run_data = batch_run.get_model_vars_dataframe()
run_data.head()

run_data.to_csv("data/"+exp_desc+".zip", index=False, compression=dict(method='zip', archive_name='data.csv'))

#%%
# run_data = pd.read_csv(os.path.dirname(__file__) + "/data/"+exp_desc+".zip")

fig = mpl.figure.Figure(figsize=(8,8))
for i,curr_policy in enumerate(['A', 'B', 'AB', 'uniform']):

    axs = fig.add_subplot(221+i)
    plot_desc = 'game sequence: '+curr_policy+', grid=(' + str(grid_width) +','+str(grid_height) +')'
    axs.grid()
    axs.scatter(run_data[(run_data.default_policy==curr_policy)]["N"], run_data[(run_data.default_policy==curr_policy)]['Gini index'], marker='x')
    #axs.set_xlabel('Number of agents')
    axs.set_xlim((1,100))
    axs.set_ylim((-0.01,1))
    # axs.set_ylabel('Gini index')
    axs.set_title(plot_desc)

display(fig)

fig.tight_layout()
fig.savefig("plots/"+ exp_desc +".pdf")
