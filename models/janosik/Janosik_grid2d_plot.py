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

script_path = ""

import os
try:
    script_path = os.path.dirname(__file__)
    os.chdir(script_path)
except FileNotFoundError:
    script_path = os.getcwd()
else:
    script_path = os.getcwd()

import sys
sys.path.append("..")


##############################################################################
############################ DATA VISUALIZATION ##############################
##############################################################################

#%% simulation parameters for batch execution
# initial capital
init_wealth = 2

# bias in the Parronod scheme
default_eps = 0.005

# size of the grid
grid_width = 10
grid_height = 10

#%% paramteres used during the simulations
#
iterations = 20
max_steps = 500

exp_desc = "grid_"+str(grid_width)+'x'+str(grid_height)+"_"+str(iterations)+"runs_"+str(max_steps)+"steps_" + str(default_eps)


#%% read data from file
rd = pd.read_csv(script_path + "/../data/"+exp_desc+".zip")
gini_data = np.loadtxt(script_path+"/../data/gini_index_values.dat")

# %% plot data

plot_label = {"matthew" : "Matthew", "antimatthew" : "anti-Matthew", "strongmatthew" : "strong Matthew", "strongantimatthew": "strong anti-Matthew"}
plot_marker = {"matthew" : "bx", "antimatthew" : "go", "strongmatthew": "r+", "strongantimatthew": "k^"}
plt_marker_size = {"matthew" : 32}
gini_min = {}
gini_max = {}
poly_app_deg = 2
x_vals = range(10,101,20)
x_vals_dense = range(10,101,1)

#%% ploting
fig = mpl.figure.Figure(figsize=(8,8))
for i,curr_policy in enumerate(['A', 'B', 'AB', 'uniform']):

    axs = fig.add_subplot(221+i)
    plot_desc = curr_policy#+r", grid("+str(grid_width)+'x'+str(grid_height)+')'
    axs.grid(alpha=0.5,ls='--')
    
    axs.plot(x_vals_dense,gini_data[x_vals_dense],'k-.')
    
    for b in ["matthew", "antimatthew", "strongmatthew", "strongantimatthew" ]:
        gini_max[b] = [rd[(rd.default_policy==curr_policy) & (rd.default_boost == b)][rd.num_agents==r]['Gini index'].max() for r in x_vals]
        gini_min[b] = [rd[(rd.default_policy==curr_policy) & (rd.default_boost == b)][rd.num_agents==r]['Gini index'].min() for r in x_vals]
   
    
        axs.plot(x_vals, gini_max[b], plot_marker[b], label=plot_label[b])
        axs.plot(x_vals, np.polyval(np.polyfit(x_vals,gini_max[b],poly_app_deg),x_vals), plot_marker[b][0]+":", linewidth=2)
        
        axs.plot(x_vals, gini_min[b], plot_marker[b])
        axs.plot(x_vals, np.polyval(np.polyfit(x_vals,gini_min[b],poly_app_deg),x_vals), plot_marker[b][0]+":", linewidth=2)
    
        # axs.plot(gini_data)
        # axs.plot(x_vals_dense, gini_data[x_vals_dense],"k",linewidth=1, markersize=4)
        #axs.set_xlabel('Number of agents')
        axs.set_xlim((2,x_vals[-1]+15))
        axs.set_ylim((0.0,1))
        # axs.set_ylabel('Gini index')
        axs.legend(ncol=1, columnspacing=0, labelspacing=0.5)
        axs.set_title(plot_desc)

display(fig)

fig.tight_layout()
fig.savefig("../plots/"+ exp_desc +".pdf")
fig.savefig("../plots/png/"+ exp_desc +".png")
