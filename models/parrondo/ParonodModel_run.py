# %%

import os
os.chdir(os.path.dirname(__file__))

# %%
import matplotlib as mpl

mpl.rc('text', usetex = True)
mpl.rc('font', size = 14)

from IPython.core.display import display

from ParrondoModel import ParrondoModel

# %%
# store data from num_runs
num_runs = 1000

# each run has num_steps steps
num_steps = 100

# each model has num_agents agents
num_agents = 10

# data from all simulations
wealth_data = []
social_data = []

for _ in range(num_runs):
    # create a model
    model = ParrondoModel(num_agents)

    # execute num_steps steps
    for _ in range(num_steps):
        model.step()
        
    for a in model.schedule.agents:
        wealth_data.append(a.wealth)
        social_data.append(abs(a.wealth-100))

# print(wealth_data)

# %%
fig = mpl.figure.Figure(figsize=(4,3))
axs = fig.add_subplot()
axs.hist(wealth_data, density=True, histtype='step')
display(fig)

# %%
fig = mpl.figure.Figure(figsize=(4,3))
axs = fig.add_subplot()
axs.hist(social_data, density=True, histtype='step')
display(fig)

# %%
# print(social_data)
