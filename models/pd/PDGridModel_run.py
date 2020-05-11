#%%
import sys
import os

sys.path.append(os.path.dirname(__file__))

from PDGridModel import PDGridModel, defectors_rate

#%%
import mesa.batchrunner as mb

import matplotlib as mpl
mpl.rc('text', usetex = True)
mpl.rc('font', size = 14)

from IPython.core.display import display

import numpy as np

#%%

# store data from 100 num_runs
num_runs = 20

# each run has num_steps steps
num_steps = 10

# dimensions of the lattice
width, height = (20,20)

# difference between payoffs in PD game
temptation = 1

# number of active agents
num_agents = int(width*height/2)

# data from all simulations
strategy_data = []
wealth_data = []


# In[]
fixed_params = {
        "width": width,
        "height": height,
        "N": num_agents        
        }

variable_params = { "temptation" : np.arange(0,4,0.5) }

batch_run = mb.BatchRunner(
        PDGridModel,
        variable_params,
        fixed_params,
        iterations=num_runs,
        max_steps=num_steps,
        model_reporters={"Defectors_rate": defectors_rate}
        )

batch_run.run_all()

# In[]

run_data = batch_run.get_model_vars_dataframe()
run_data.head()
print(run_data)

# In[]

fig = mpl.figure.Figure(figsize=(4,3))
axs = fig.add_subplot(111)
axs.set_xlabel("Temptation")
axs.set_ylabel("Fraction of defectors")
axs.scatter(run_data.temptation, run_data.Defectors_rate)

display(fig)

