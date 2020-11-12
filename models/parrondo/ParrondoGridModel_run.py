#!/usr/bin/env python
# coding: utf-8

#%% global packages
import mesa.batchrunner as mb
import numpy as np

from IPython.core.display import display

import matplotlib as mpl
# import matplotlib.figure as figure
mpl.rc('text', usetex = True)
mpl.rc('font', size = 10)


#%% local functions

import os
os.chdir(os.path.dirname(__file__))

from ParrondoGridModel import ParrondoGridModel

import sys
sys.path.append("..")

import indicators

#%% simulation parameters

# initial capital
init_wealth = 100

# bias in the Parronod scheme
default_policy = 'A'
default_eps = 0.002

# store data from num_runs
num_runs = 1

# each run has num_steps steps
num_steps = 5000

# size of the grid
grid_width = 15
grid_height = 15

# each model has num_agents agents
num_agents = grid_width*grid_height

# data from all simulations
wealth_data = []
agent_counts = np.zeros((grid_width, grid_height))

# strin with descriptions used in plots
plot_desc = 'game sequence: '+default_policy+', grid=(' + str(grid_width) +','+str(grid_height) +')'

#%% simulaiton with fixed parameters

for _ in range(num_runs):
    # create a model
    model = ParrondoGridModel(num_agents, grid_width, grid_height, init_wealth, default_policy, default_eps)

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

#%% plot of the mean wealth

data = model.datacollector.get_model_vars_dataframe()
median_wealth_data=data.get('Median wealth')
median_wealth_data.plot(title='Median wealth, ' + plot_desc, ylim=(0,200))

print(median_wealth_data.describe())


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





#%%
# 
# Batch execution of the simulations
#


fixed_params = {
        "width": grid_width,
        "height": grid_height,
        "init_wealth": init_wealth,
        "default_eps": default_eps
        }

variable_params = { 
        "N" : range(10, 100, 5),
        "default_policy" : ['A', 'B', 'AB', 'uniform']
        }
         
batch_run = mb.BatchRunner(
        ParrondoGridModel,
        variable_parameters=variable_params,
        fixed_parameters=fixed_params,
        iterations=100,
        max_steps=500,
        model_reporters={
            "Gini index" : indicators.gini_index,
            "Total wealth" : indicators.total_wealth,
            "Mean wealth" : indicators.mean_wealth
            }
        )

batch_run.run_all()

#%%
run_data = batch_run.get_model_vars_dataframe()
run_data.head()

fig = mpl.figure.Figure(figsize=(8,8))
for i,curr_policy in enumerate(['A', 'B', 'uniform', 'AB']):#= 'A'

    axs = fig.add_subplot(221+i)
    plot_desc = 'game sequence: '+curr_policy+', grid=(' + str(grid_width) +','+str(grid_height) +')'
    axs.scatter(run_data[(run_data.default_policy==curr_policy)].N,run_data[(run_data.default_policy==curr_policy)]['Gini index'],marker='x')
    #axs.set_xlabel('Number of agents')
    axs.set_xlim((1,50))
    axs.set_ylim((-0.01,0.3))
    # axs.set_ylabel('Gini index')
    axs.set_title(plot_desc)

display(fig)

exp_desc = "grid_"+str(grid_width)+'x'+str(grid_height)+"_"+str(batch_run.iterations)+"runs_"+str(batch_run.max_steps)+"steps"

fig.tight_layout()
fig.savefig("plots/"+ exp_desc +".pdf")

#%%
run_data.to_csv("data/"+exp_desc+".zip", index=False, compression=dict(method='zip', archive_name='data.csv'))



