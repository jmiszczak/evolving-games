#%%

from PDGridModel import PDGridModel, defectors_rate

#%%
import mesa.batchrunner as mb

import matplotlib as mpl
mpl.rc('text', usetex = True)
mpl.rc('font', size = 14)

from IPython.core.display import display

#%%

# store data from 100 num_runs
num_runs = 50

# each run has num_steps steps
num_steps = 10

# dimensions of the lattice
width, height = (20,20)

# difference between payoffs in PD game
temptation = 1

# number of active agents
num_agents = 2*width*height

# data from all simulations
strategy_data = []


# In[]
fixed_params = {
        "width": width,
        "height": height,
        "temptation": temptation
        }

variable_params = { "N" : range(10, 101, 10) }

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
axs.scatter(run_data.N, run_data.Defectors_rate)

display(fig)

