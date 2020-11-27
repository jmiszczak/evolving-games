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
import matplotlib.markers as markers
mpl.rc('text', usetex = True)
mpl.rc('font', size = 9)


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
max_steps = 300

# values of the bias used in the experiments
eps_vals =  [0.0]+list(-1*np.array([0.025, 0.05, 0.10, 0.125, 0.15, 0.25, 0.3, 0.5]))

exp_desc = 'janosik_'+"grid_"+str(grid_width)+'x'+str(grid_height)+"_"+str(iterations)+"runs_"+str(max_steps)+"steps"#"_" + str(default_eps)+"eps"


#%% results form the batch execution
# rd.columns = ['num_agents', 'default_boost', 'default_eps', 'Run', 'Gini index', 'Total capital', 'Mean capital', 'Median capital', 'Min capital', 'Max capital', 'graph_spec', 'init_wealth']
# rd.to_csv("data/"+exp_desc+".zip", index=False, compression=dict(method='zip', archive_name='data.csv'))

# %% plot Gini data
plot_label = {"matthew" : "Matthew", "antimatthew" : "anti-Matthew", "strongmatthew" : "strong Matthew", "strongantimatthew": "strong anti-Matthew"}
plot_marker = {"matthew" : "bs", "antimatthew" : "go", "strongmatthew": "rx", "strongantimatthew": "k+"}
plt_marker_size = {"matthew" : 5, "antimatthew": 5, "strongmatthew": 6, "strongantimatthew": 6}
gini_min = {}
gini_max = {}
poly_app_deg = 2
x_vals = range(20,141,20)
x_vals_dense = range(20,141,10)

#%% load data

# data from the experiement
rd = pd.read_csv(script_path + "/data/"+exp_desc+".zip")
# rd.columns = ['num_agents', 'default_boost', 'default_eps', 'Run', 'Gini index', 'Total capital', 'Mean capital', 'Median capital', 'Min capital', 'Max capital', 'graph_spec', 'init_wealth']

# initial values of Gini
gini_data = np.loadtxt(script_path+"/data/gini_index_values-constant.dat")

#%% ploting

fig = mpl.figure.Figure(figsize=(6.5,4.875))
for i,curr_eps in enumerate(eps_vals ):

    axs = fig.add_subplot(331+i)
    plot_desc = r'$\epsilon=$ '+str(curr_eps)#+r", grid("+str(grid_width)+'x'+str(grid_height)+')'
    axs.grid(alpha=0.75,ls=':')
    
    axs.plot(x_vals_dense,gini_data[x_vals_dense],'k-.')
    
    for b in ["matthew", "strongmatthew", "antimatthew", "strongantimatthew" ]:
        gini_max[b] = [rd[(rd.default_eps==curr_eps) & (rd.default_boost == b)][rd.num_agents==r]['Gini index'].max() for r in x_vals]
        gini_min[b] = [rd[(rd.default_eps==curr_eps) & (rd.default_boost == b)][rd.num_agents==r]['Gini index'].min() for r in x_vals]
   
        axs.plot(x_vals, gini_max[b], plot_marker[b], fillstyle='none', ms=plt_marker_size[b], label=plot_label[b])
        axs.plot(x_vals, np.polyval(np.polyfit(x_vals,gini_max[b],poly_app_deg),x_vals), plot_marker[b][0]+":", linewidth=1)
    
        axs.plot(x_vals, gini_min[b], plot_marker[b],  fillstyle='none', ms=plt_marker_size[b] )
        axs.plot(x_vals, np.polyval(np.polyfit(x_vals,gini_min[b],poly_app_deg),x_vals), plot_marker[b][0]+":", linewidth=1)
   
        # axs.plot(gini_data)
        # axs.plot(x_vals_dense, gini_data[x_vals_dense],"k",linewidth=1, markersize=4)

        axs.set_xlim((2,x_vals[-1]+15))
        axs.set_ylim((-0.05,0.85))

        axs.text(15, 0.73, plot_desc, rasterized=False, usetex=True)
        axs.set_xticks(x_vals)
                    
        if i in [6,7,8]:
            axs.set_xlabel('Number of agents')
        else:
            axs.set_xticklabels([])           
            
        axs.set_yticks(np.arange(0, 1, step=0.2))
            
        if i in [0,3,6]:
            axs.set_ylabel('Gini index')
        else:
            axs.set_yticklabels([])

            
handles, labels = axs.get_legend_handles_labels()
lgd = fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.525,1.05), ncol=4)

display(fig)

fig.tight_layout()
fig.savefig("plots/"+ exp_desc +".pdf", bbox_extra_artists=(lgd,), bbox_inches='tight')
fig.savefig("plots/png/"+ exp_desc +".png")
