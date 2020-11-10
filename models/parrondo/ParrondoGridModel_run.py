#!/usr/bin/env python
# coding: utf-8

#%%
from IPython.core.display import display

import numpy as np

import matplotlib as mpl
import matplotlib.figure as figure
# mpl.rc('text', usetex = True)
mpl.rc('font', size = 14)


#%% local definitions

import os
os.chdir(os.path.dirname(__file__))

from ParrondoGridModel import ParrondoGridModel

import mesa.batchrunner as mb


#%%
import sys
sys.path.append("..")

import indicators

#%%

# initial capital
init_wealth = 10

# bias in the Parronod scheme
default_policy = 'uniform'
default_eps = 0.05

# store data from num_runs
num_runs = 1

# each run has num_steps steps
num_steps = 2500

# size of the grid
grid_width = 6
grid_height = 6

# each model has num_agents agents
num_agents = grid_width*grid_height*10

# data from all simulations
wealth_data = []
agent_counts = np.zeros((grid_width, grid_height))

#%%

for _ in range(num_runs):
    # create a model
    model = ParrondoGridModel(num_agents, grid_width, grid_height, init_wealth, default_policy, default_eps)

    # execute num_steps steps
    for _ in range(num_steps):
        model.step()
        
    for a in model.schedule.agents:
        wealth_data.append(a.wealth)

#%%

gini = model.datacollector.get_model_vars_dataframe()
gini.plot(title=default_policy, ylim=(0.2,0.5))

# print(gini.describe())

#%%
# fig = figure.Figure(figsize=(8,6))
# axs = fig.add_subplot()
# axs.hist(wealth_data, density=True, histtype='step',bins=int(num_runs/2))
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



#%%
agent_wealth = model.datacollector.get_agent_vars_dataframe()
print(agent_wealth.head())

one_agent_wealth = agent_wealth.xs(1, level="AgentID")
one_agent_wealth.Wealth.plot()


#%%
# 
# Batch execution of the simulations
#


fixed_params = {
        "width": grid_width,
        "height": grid_height,
        "init_wealth": init_wealth,
        "default_policy": default_policy, 
        "default_eps": default_eps
        }

variable_params = { "N" : range(36, 73, 24)}

batch_run = mb.BatchRunner(
        ParrondoGridModel,
        variable_parameters=variable_params,
        fixed_parameters=fixed_params,
        iterations=5,
        max_steps=1000,
        model_reporters={"Gini": indicators.gini}
        )

batch_run.run_all()


#%%
run_data = batch_run.get_model_vars_dataframe()
run_data.head()

fig = mpl.figure.Figure(figsize=(8,8))
axs = fig.add_subplot()
axs.scatter(run_data.N, run_data.Gini)
axs.set_xlabel('Number of agents')
axs.set_ylabel('Gini index')
axs.set_title(default_policy+ ", eps=" +str(default_eps))
display(fig)


#%%
run_data.to_csv('ParrondoGridModel.zip', index=False, compression=dict(method='zip', archive_name='data.csv'))



