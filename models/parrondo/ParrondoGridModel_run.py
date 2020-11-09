#!/usr/bin/env python
# coding: utf-8

#%%
from IPython.core.display import display

import numpy as np

import matplotlib as mpl
import matplotlib.figure as figure
mpl.rc('text', usetex = True)
mpl.rc('font', size = 14)


#%% local definitions

import os
os.chdir(os.path.dirname(__file__))

from ParrondoGridModel import ParrondoGridModel

#%%
import sys
sys.path.append("..")

import indicators

#%%
init_wealth = 20

# store data from num_runs
num_runs = 10

# each run has num_steps steps
num_steps = 100

# each model has num_agents agents
num_agents = 500

# size of the grid
grid_width = 50
grid_height = 50

# data from all simulations
wealth_data = []
agent_counts = np.zeros((grid_width, grid_height))

#%%

for _ in range(num_runs):
    # create a model
    model = ParrondoGridModel(num_agents, grid_width, grid_height, init_wealth)

    # execute num_steps steps
    for _ in range(num_steps):
        model.step()
        
    for a in model.schedule.agents:
        wealth_data.append(a.wealth)


#%%
fig = figure.Figure(figsize=(8,6))
axs = fig.add_subplot()
axs.hist(wealth_data, density=True, histtype='step')
display(fig)


#%%
for cell in model.grid.coord_iter():
    cell_content, x, y = cell
    agent_counts[x][y] = len(cell_content)    


#%%
fig = mpl.figure.Figure(figsize=(8,8))
axs = fig.add_subplot()

axs.imshow(agent_counts, interpolation='none', cmap=mpl.cm.Greys)
norm = mpl.cm.colors.Normalize(vmin=agent_counts.min(), vmax=agent_counts.max())
fig.colorbar(mpl.cm.ScalarMappable(cmap=mpl.cm.Greys, norm=norm), ax=axs)

display(fig)

#%%

gini = model.datacollector.get_model_vars_dataframe()
gini.plot()

print(gini.describe())

#%%
agent_wealth = model.datacollector.get_agent_vars_dataframe()
print(agent_wealth.head())

one_agent_wealth = agent_wealth.xs(20, level="AgentID")
one_agent_wealth.Wealth.plot()


#%%
# 
# Batch execution of the simulations
#

from ParrondoGridModel import ParrondoGridModel
import mesa.batchrunner as mb

fixed_params = {
        "width": 50,
        "height": 50,
        "init_wealth": 20
        }

variable_params = { "N" : range(50, 500, 50)}

batch_run = mb.BatchRunner(
        ParrondoGridModel,
        variable_parameters=variable_params,
        fixed_parameters=fixed_params,
        iterations=10,
        max_steps=10,
        model_reporters={"Gini": indicators.gini}
        )

batch_run.run_all()


#%%
run_data = batch_run.get_model_vars_dataframe()
run_data.head()


#%%
fig = mpl.figure.Figure(figsize=(8,8))
axs = fig.add_subplot()
axs.scatter(run_data.N, run_data.Gini)
display(fig)


#%%
run_data.to_csv('ParrondoGridModel.zip', index=False, compression=dict(method='zip', archive_name='data.csv'))



