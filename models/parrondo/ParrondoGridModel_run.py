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

# initial capital
init_wealth = 100

# bias in the Parronod scheme
default_policy = 'uniform'
default_eps = 0.1

# store data from num_runs
num_runs = 20

# each run has num_steps steps
num_steps = 100

# each model has num_agents agents
num_agents = 20

# size of the grid
grid_width = 10
grid_height = 10

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



# %%
# fig = figure.Figure(figsize=(8,6))
# axs = fig.add_subplot()
# axs.hist(wealth_data, density=True, histtype='step',bins=int(num_runs/2))
# axs.set_xlabel('Wealth')
# display(fig)


# %%
# for cell in model.grid.coord_iter():
#     cell_content, x, y = cell
#     agent_counts[x][y] = len(cell_content)    


# %%
# fig = mpl.figure.Figure(figsize=(8,8))
# axs = fig.add_subplot()

# axs.imshow(agent_counts, interpolation='none', cmap=mpl.cm.Greys)
# norm = mpl.cm.colors.Normalize(vmin=agent_counts.min(), vmax=agent_counts.max())
# fig.colorbar(mpl.cm.ScalarMappable(cmap=mpl.cm.Greys, norm=norm), ax=axs)

# display(fig)

#%%

gini = model.datacollector.get_model_vars_dataframe()
gini.plot(title=default_policy)

print(gini.describe())

#%%
agent_wealth = model.datacollector.get_agent_vars_dataframe()
print(agent_wealth.head())

one_agent_wealth = agent_wealth.xs(11, level="AgentID")
one_agent_wealth.Wealth.plot()


#%%
# 
# Batch execution of the simulations
#

from ParrondoGridModel import ParrondoGridModel
import mesa.batchrunner as mb

fixed_params = {
        "width": grid_width,
        "height": grid_height,
        "init_wealth": init_wealth,
        "default_policy": default_policy, 
        "default_eps": default_eps
        }

variable_params = { "N" : range(50, 250, 50)}

batch_run = mb.BatchRunner(
        ParrondoGridModel,
        variable_parameters=variable_params,
        fixed_parameters=fixed_params,
        iterations=30,
        max_steps=50,
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
display(fig)


#%%
run_data.to_csv('ParrondoGridModel.zip', index=False, compression=dict(method='zip', archive_name='data.csv'))



