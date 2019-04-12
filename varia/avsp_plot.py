from configparser import ConfigParser
from pathlib import Path
from sys import argv

import numpy as np

import matplotlib.pyplot as plt

# read configuration for the simulation
avsp_config = ConfigParser()
avsp_config.read('avsp_config.ini')
default_run = 'default'  # must be defined in the config file!

# read the name of the config section to be used in the current run
try:
    run_name = argv[1]
except:
    run_name = default_run
    print("[WARNING] Specify the name of the run (section in *.ini file)!")
    print("[WARNING] Using run '", run_name, "'.", sep="")

# read simulation parameters for the current run
try:
    dim1 = int(avsp_config[run_name]['dim1'])
    dim2 = int(avsp_config[run_name]['dim2'])
    max_steps = int(avsp_config[run_name]['max_steps'])
    repeat_times = int(avsp_config[run_name]['repeat_times'])
except KeyError:
    print("[ERROR] Problem while reading section", run_name, "from the config file.")
    exit(1)

# preapre the figure and the axis
fig = plt.figure()
ax = fig.add_subplot(111)


data_path = Path("avsp_results/"+run_name+".npz")
data = np.load(data_path)

data_mean = [0]*len(data[data.keys()[1]])

for k in data.keys():
    data_mean = data_mean + data[k]

data_mean = data_mean/repeat_times

ax.plot(range(0, max_steps), data_mean)
plt.savefig('avsp_plots/' + run_name + '.pdf')

plt.show()


