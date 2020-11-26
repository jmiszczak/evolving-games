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
mpl.rc('font', size = 12)


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

from JanosikGraphModel import JanosikGraphModel
import indicators

##############################################################################
############################## BATCH EXECUTION ###############################
##############################################################################

#%% simulation parameters for batch execution

# initial capital
init_capital = 2

# bias in the game
default_eps = 0.15

# size of the grid
grid_width = 10
grid_height = 10

# graph used in the experiments
graph = nx.generators.lattice.grid_2d_graph(grid_width,grid_height,periodic=True)

graph_id = "w"+str(grid_width) + "_h"+str(grid_height)
graph_file_path = script_path + '/graphs/grid2d/' + graph_id + ".gz"
nx.readwrite.write_gexf(graph, graph_file_path)
# nx.draw(graph)

eps_vals =  [0.0, 0.025, 0.05, 0.10, 0.125, 0.15, 0.25, 0.3, 0.5]

#%% batch execution of the simulations
#

fixed_params = {
        "graph_spec": graph_file_path,
        "init_capital": init_capital
        }

variable_params = { 
        "num_agents" : range(20, 121, 20),
        "default_boost" : ["matthew", "antimatthew", "strongmatthew" ,"strongantimatthew"],
        "default_eps" : eps_vals 
        }
         
batch_run = mb.BatchRunnerMP(
        JanosikGraphModel,
        nr_processes = 8,
        variable_parameters=variable_params,
        fixed_parameters=fixed_params,
        iterations=5,
        max_steps=5,
        model_reporters={
            "Gini index" : indicators.gini_index,
            "Total capital": indicators.total_capital, 
            "Mean capital": indicators.mean_capital,
            "Median capital": indicators.median_capital,
            "Min capital": indicators.min_capital,
            "Max capital": indicators.max_capital 
            }
        )

exp_desc = 'janosik_'+"grid_"+str(grid_width)+'x'+str(grid_height)+"_"+str(batch_run.iterations)+"runs_"+str(batch_run.max_steps)+"steps"#"_" + str(default_eps)+"eps"
#%% run the experiment
print("[INFO] Executing", len(variable_params["num_agents"])*len(variable_params["default_boost"])*len(variable_params["default_eps"])*batch_run.iterations, "iterations.", flush=True)
batch_run.run_all()

#%% results form the batch execution
rd =  batch_run.get_model_vars_dataframe()
# workaround for the Mesa bug
rd.columns = ['num_agents', 'default_boost', 'default_eps', 'Run', 'Gini index', 'graph_spec', 'init_wealth']

rd.to_csv("data/"+exp_desc+".zip", index=False, compression=dict(method='zip', archive_name='data.csv'))

# %% plot data

plot_label = {"matthew" : "Matthew", "antimatthew" : "anti-Matthew", "strongmatthew" : "strong Matthew", "strongantimatthew": "strong anti-Matthew"}
plot_marker = {"matthew" : "bx", "antimatthew" : "go", "strongmatthew": "r+", "strongantimatthew": "k^"}
plt_marker_size = {"matthew" : 32}
gini_min = {}
gini_max = {}
poly_app_deg = 2
x_vals = range(20,121,20)
x_vals_dense = range(20,121,10)
gini_data = np.loadtxt(script_path+"/data/gini_index_values-constant.dat")


#%% ploting
fig = mpl.figure.Figure(figsize=(12,10))
for i,curr_eps in enumerate(eps_vals ):

    axs = fig.add_subplot(331+i)
    plot_desc = r'$\epsilon=$ '+str(curr_eps)#+r", grid("+str(grid_width)+'x'+str(grid_height)+')'
    axs.grid(alpha=0.5,ls='--')
    
    axs.plot(x_vals_dense,gini_data[x_vals_dense],'k-.')
    
    for b in ["matthew", "strongmatthew", "antimatthew", "strongantimatthew" ]:
        gini_max[b] = [rd[(rd.default_eps==curr_eps) & (rd.default_boost == b)][rd.num_agents==r]['Gini index'].max() for r in x_vals]
        gini_min[b] = [rd[(rd.default_eps==curr_eps) & (rd.default_boost == b)][rd.num_agents==r]['Gini index'].min() for r in x_vals]
   
    
        axs.plot(x_vals, gini_max[b], plot_marker[b], label=plot_label[b])
        axs.plot(x_vals, np.polyval(np.polyfit(x_vals,gini_max[b],poly_app_deg),x_vals), plot_marker[b][0]+":", linewidth=1)
        
        axs.plot(x_vals, gini_min[b], plot_marker[b])
        axs.plot(x_vals, np.polyval(np.polyfit(x_vals,gini_min[b],poly_app_deg),x_vals), plot_marker[b][0]+":", linewidth=1)
        
    # axs.scatter(run_data[(run_data.default_policy==curr_policy) & (run_data.default_boost == 'antimatthew')].num_agents, 
    #             run_data[(run_data.default_policy==curr_policy) & (run_data.default_boost == 'antimatthew')]['Gini index'],
    #             marker='*',color='k', s=24, label="anti-Matthew")
    
    # axs.scatter(run_data[(run_data.default_policy==curr_policy) & (run_data.default_boost == 'strongmatthew')].num_agents, 
    #             run_data[(run_data.default_policy==curr_policy) & (run_data.default_boost == 'strongmatthew')]['Gini index'],
    #             marker='^',color='b', s=38, label="strong pro-Matthew")

    
    # axs.scatter(run_data[(run_data.default_policy==curr_policy) & (run_data.default_boost == 'strongantimatthew')].num_agents, 
    #             run_data[(run_data.default_policy==curr_policy) & (run_data.default_boost == 'strongantimatthew')]['Gini index'],
    #             marker='x',color='g', s=24, label="strong anti-Matthew")
    
        # axs.plot(gini_data)

        # axs.plot(x_vals_dense, gini_data[x_vals_dense],"k",linewidth=1, markersize=4)
        #axs.set_xlabel('Number of agents')
        axs.set_xlim((2,x_vals[-1]+15))
        axs.set_ylim((0.05,0.6))
        # axs.set_ylabel('Gini index')
        # axs.legend(ncol=1, columnspacing=0, labelspacing=0.5)
        axs.set_title(plot_desc)

handles, labels = axs.get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(0.5,-0.02), ncol=4)

display(fig)

fig.tight_layout()
fig.savefig("plots/"+ exp_desc +".pdf")
fig.savefig("plots/png/"+ exp_desc +".png")



# #%% ploting
# fig = mpl.figure.Figure(figsize=(6,3/4*6))

# axs = fig.add_subplot()
# plot_desc = ""#curr_policy#+r", grid("+str(grid_width)+'x'+str(grid_height)+')'
# axs.grid(alpha=0.5,ls='--')

# axs.plot(x_vals_dense,gini_data[x_vals_dense],'k-.')

# for b in ["matthew", "strongmatthew", "antimatthew", "strongantimatthew" ]:
#     gini_max[b] = [rd[(rd.default_boost == b)][rd.num_agents==r]['Gini index'].max() for r in x_vals]
#     gini_min[b] = [rd[(rd.default_boost == b)][rd.num_agents==r]['Gini index'].min() for r in x_vals]
   

#     axs.plot(x_vals, gini_max[b], plot_marker[b], label=plot_label[b])
#     axs.plot(x_vals, np.polyval(np.polyfit(x_vals,gini_max[b],poly_app_deg),x_vals), plot_marker[b][0]+":", linewidth=1)
    
#     axs.plot(x_vals, gini_min[b], plot_marker[b])
#     axs.plot(x_vals, np.polyval(np.polyfit(x_vals,gini_min[b],poly_app_deg),x_vals), plot_marker[b][0]+":", linewidth=2)

#     # axs.plot(gini_data)
#     axs.plot(x_vals_dense, gini_data[x_vals_dense],"ok",linewidth=1, markersize=4)
#     #axs.set_xlabel('Number of agents')
#     axs.set_xlim((12,x_vals[-1]+8))
#     axs.set_ylim((-.2,2.1))
#     # axs.set_ylabel('Gini index')
#     axs.legend(ncol=2, columnspacing=0, labelspacing=0.5)
#     axs.set_title(plot_desc)

# display(fig)

# fig.tight_layout()
# fig.savefig("plots/"+ exp_desc +".pdf")
# fig.savefig("plots/png/"+ exp_desc +".png")
