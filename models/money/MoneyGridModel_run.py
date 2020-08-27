#!/usr/bin/env python
# coding: utf-8

# %%
from IPython.core.display import display

import numpy as np

import matplotlib as mpl
import matplotlib.figure as figure
mpl.rc('text', usetex = True)
mpl.rc('font', size = 14)

import os
os.chdir(os.path.dirname(__file__))

from MoneyGridModel import MoneyGridModel

import sys
sys.path.append('../')
print(sys.path)

import indicators


# %%

# store data from num_runs
num_runs = 100

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


# %%

for _ in range(num_runs):
    # create a model
    model = MoneyGridModel(num_agents, grid_width, grid_height)

    # execute num_steps steps
    for _ in range(num_steps):
        model.step()
        
    for a in model.schedule.agents:
        wealth_data.append(a.wealth)


# %%
fig = figure.Figure(figsize=(8,6))
axs = fig.add_subplot()
axs.hist(wealth_data, density=True, histtype='step')
display(fig)


# %%
for cell in model.grid.coord_iter():
    cell_content, x, y = cell
    agent_counts[x][y] = len(cell_content)    


# %%
fig = mpl.figure.Figure(figsize=(8,8))
axs = fig.add_subplot()

axs.imshow(agent_counts, interpolation='none', cmap=mpl.cm.Greys)
norm = mpl.cm.colors.Normalize(vmin=agent_counts.min(), vmax=agent_counts.max())
fig.colorbar(mpl.cm.ScalarMappable(cmap=mpl.cm.Greys, norm=norm), ax=axs)

display(fig)

# %%

gini = model.datacollector.get_model_vars_dataframe()
gini.plot()

# %%

print(gini.describe())

# %%
# 
# Batch execution of the simulations
#

from MoneyGridModel import MoneyGridModel
import mesa.batchrunner as mb

fixed_params = {
        "width": 10,
        "height": 10
        }

variable_params = { "N" : range(10, 500, 10)}

batch_run = mb.BatchRunner(
        MoneyGridModel,
        variable_params,
        fixed_params,
        iterations=5,
        max_steps=100,
        model_reporters={"Gini": indicators.gini}
        )

batch_run.run_all()


# %%
run_data = batch_run.get_model_vars_dataframe()
run_data.head()


# %%
fig = mpl.figure.Figure(figsize=(8,8))
axs = fig.add_subplot()
axs.scatter(run_data.N, run_data.Gini)
display(fig)


# %%
run_data.to_csv('MoneyGridModel.zip', index=False, compression=dict(method='zip', archive_name='data.csv'))


