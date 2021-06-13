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

from JanosikParrondoGraphModel import JanosikParrondoGraphModel
import indicators

##############################################################################
############################## BATCH EXECUTION ###############################
##############################################################################

#%% simulation parameters for batch execution

# initial capital
init_capital = 20

# size of the grid
grid_width = 10
grid_height = 10

# graph used in the experiments
graph_id = "w"+str(grid_width) + "_h"+str(grid_height)
graph_file_path = script_path + '/graphs/grid2d/' + graph_id + ".gz"

# graph generation and saving - can be used only onece for the grid
# graph = nx.generators.lattice.grid_2d_graph(grid_width,grid_height,periodic=True)
# nx.readwrite.write_gexf(graph, graph_file_path)
# nx.draw(graph)

# bias in the Parronod scheme, policy, number of agents
default_policies = ['A', 'B', 'AABB', 'uniform']
default_eps_vals = [0.1, 0.05, 0.01, 0.005]
agen_nums = range(20,121,20)

#%% batch execution of the simulations
#

fixed_params = {
        "graph_spec": graph_file_path,
        "init_capital": init_capital,
        }

variable_params = { 
        "num_agents" : agen_nums,
        "default_policy" : default_policies,
        "default_eps": default_eps_vals,
        "default_boost" : ["matthew", "antimatthew", "strongmatthew" ,"strongantimatthew"]
        }
         
batch_run = mb.BatchRunnerMP(
        JanosikParrondoGraphModel,
        nr_processes = 8,
        variable_parameters=variable_params,
        fixed_parameters=fixed_params,
        iterations=10,
        max_steps=300,
        model_reporters={
            "Gini index" : indicators.gini_index,
            "Hoover index" : indicators.hoover_index,

            }
        )

exp_desc = "janosik-parrondo_grid_"+str(grid_width)+'x'+str(grid_height)+"_"+str(batch_run.iterations)+"runs_"+str(batch_run.max_steps)+"steps"
#%% run the experiment
if __name__ == "__main__":
    print("[INFO] Executing", np.prod(list(map(len,variable_params.values())))*batch_run.iterations, "iterations.", flush=True)
    batch_run.run_all()

    #%% results form the batch execution
    rd =  batch_run.get_model_vars_dataframe()
    # workaround for the Mesa bug
    rd.columns = ['num_agents', 'default_policy', 'default_eps', 'default_boost', 'Run', 'Gini index', 'Hoover index', 'graph_spec', 'init_wealth']
    rd.to_csv("data/"+exp_desc+".zip", index=False, compression=dict(method='zip', archive_name='data.csv'))
    print("[INFO] Data saved to: " + "data/"+exp_desc+".zip")

# # %% plot Gini data
# plot_label = {"matthew" : "Matthew", "antimatthew" : "anti-Matthew", "strongmatthew" : "strong Matthew", "strongantimatthew": "strong anti-Matthew"}
# plot_marker = {"matthew" : "bs", "antimatthew" : "go", "strongmatthew": "rx", "strongantimatthew": "k+"}
# plt_marker_size = {"matthew" : 5, "antimatthew": 5, "strongmatthew": 6, "strongantimatthew": 6}
# gini_min = {}
# gini_max = {}
# poly_app_deg = 2
# x_vals = agen_nums
# x_vals_dense = range(agen_nums.start,agen_nums.stop,agen_nums.step//2)
# gini_data = np.loadtxt(script_path+"/data/gini_index_values-constant.dat")
# 
# #%% ploting
# fig = mpl.figure.Figure(figsize=(12,10))
# for i,curr_policy in enumerate(default_policies):
#     for j,curr_eps in enumerate(default_eps_vals):
#         
#         axs = fig.add_subplot(4,4,1+i+4*j)
#         plot_desc = str(curr_policy)+ ", " + r"$\epsilon$="+str(curr_eps)
#         axs.grid(alpha=0.5,ls=':')
#         
#         axs.plot(x_vals_dense,gini_data[x_vals_dense],'k-.')
#         
#         for b in ["matthew", "strongmatthew", "antimatthew", "strongantimatthew" ]:
#             gini_max[b] = [rd[(rd.default_policy==curr_policy) & (rd.default_boost == b) & (rd.default_eps == curr_eps) ][rd.num_agents==r]['Gini index'].max() for r in x_vals]
#             gini_min[b] = [rd[(rd.default_policy==curr_policy) & (rd.default_boost == b) & (rd.default_eps == curr_eps) ][rd.num_agents==r]['Gini index'].min() for r in x_vals]
#        
#         
#             # axs.plot(x_vals, gini_max[b], plot_marker[b], label=plot_label[b])
#             # axs.plot(x_vals, np.polyval(np.polyfit(x_vals,gini_max[b],poly_app_deg),x_vals), plot_marker[b][0]+":", linewidth=1)
#             
#             # axs.plot(x_vals, gini_min[b], plot_marker[b])
#             # axs.plot(x_vals, np.polyval(np.polyfit(x_vals,gini_min[b],poly_app_deg),x_vals), plot_marker[b][0]+":", linewidth=1)
#             
#             
#             axs.plot(x_vals, gini_max[b], plot_marker[b], fillstyle='none', ms=plt_marker_size[b], label=plot_label[b])
#             axs.plot(x_vals, np.polyval(np.polyfit(x_vals,gini_max[b],poly_app_deg),x_vals), plot_marker[b][0]+":", linewidth=1)
#             
#             axs.plot(x_vals, gini_min[b], plot_marker[b],  fillstyle='none', ms=plt_marker_size[b] )
#             axs.plot(x_vals, np.polyval(np.polyfit(x_vals,gini_min[b],poly_app_deg),x_vals), plot_marker[b][0]+":", linewidth=1)
#             
#        
#             # axs.plot(gini_data)
#             # axs.plot(x_vals_dense, gini_data[x_vals_dense],"k",linewidth=1, markersize=4)
#             #axs.set_xlabel('Number of agents')
#             axs.set_xlim((2,x_vals[-1]+15))
#             axs.set_ylim((0.0,0.8))
#             # axs.set_ylabel('Gini index')
#             # axs.legend(ncol=1, columnspacing=0, labelspacing=0.5)
#             # axs.set_title(plot_desc)
#             
#             axs.text(15, 0.60, plot_desc, rasterized=False, usetex=True)
#             axs.set_xticks(x_vals)
# 
#             if i in [6,7,8]:
#                 axs.set_xlabel('Number of agents')
#             else:
#                 axs.set_xticklabels([])           
#                 
#             axs.set_yticks(np.arange(0, 1, step=0.2))
#                 
#             if i in [0,4,8,12]:
#                 axs.set_ylabel('Gini index')
#             else:
#                 axs.set_yticklabels([])
# 
# handles, labels = axs.get_legend_handles_labels()
# fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(0.5,-0.02), ncol=4)
# 
# display(fig)
# 
# fig.tight_layout()
# fig.savefig("plots/"+ exp_desc +".pdf")
# fig.savefig("plots/png/"+ exp_desc +".png")


# #%% results form the batch execution
# run_data =  batch_run.get_model_vars_dataframe()
# # workaround for the Mesa bug
# run_data.columns = ['num_agents', 'default_policy', 'default_boost', 'Run', 'Gini index', 'graph_spec', 'init_wealth', 'default_eps']

# run_data.to_csv("data/"+exp_desc+".zip", index=False, compression=dict(method='zip', archive_name='data.csv'))

# #%% read data from file
# run_data = pd.read_csv(script_path + "/data/"+exp_desc+".zip")
# gini_data = np.loadtxt(script_path+"/data/gini_index_values-constant.dat")

# # %% plot data
# fig = mpl.figure.Figure(figsize=(8,8))
# for i,curr_policy in enumerate(['A', 'B', 'AB', 'uniform']):

#     axs = fig.add_subplot(221+i)
#     plot_desc = 'game: '+curr_policy+", grid("+str(grid_width)+'x'+str(grid_height)+')'
#     axs.grid(alpha=0.5,ls='--')
    
#     axs.scatter(run_data[(run_data.default_policy==curr_policy) & (run_data.default_boost == 'matthew')].num_agents, 
#                 run_data[(run_data.default_policy==curr_policy) & (run_data.default_boost == 'matthew')]['Gini index'],
#                 marker='o',color='r', s=24, label="pro-Matthew")
    
    
#     axs.scatter(run_data[(run_data.default_policy==curr_policy) & (run_data.default_boost == 'antimatthew')].num_agents, 
#                 run_data[(run_data.default_policy==curr_policy) & (run_data.default_boost == 'antimatthew')]['Gini index'],
#                 marker='*',color='k', s=24, label="anti-Matthew")
    
#     axs.scatter(run_data[(run_data.default_policy==curr_policy) & (run_data.default_boost == 'strongmatthew')].num_agents, 
#                 run_data[(run_data.default_policy==curr_policy) & (run_data.default_boost == 'strongmatthew')]['Gini index'],
#                 marker='+',color='b', s=38, label="strong pro-Matthew")

    
#     axs.scatter(run_data[(run_data.default_policy==curr_policy) & (run_data.default_boost == 'strongantimatthew')].num_agents, 
#                 run_data[(run_data.default_policy==curr_policy) & (run_data.default_boost == 'strongantimatthew')]['Gini index'],
#                 marker='x',color='g', s=24, label="strong anti-Matthew")
    
#     axs.plot(gini_data,"k:")
#     #axs.set_xlabel('Number of agents')
#     axs.set_xlim((2,137))
#     axs.set_ylim((0.0,1))
#     # axs.set_ylabel('Gini index')
#     axs.legend(ncol=1, columnspacing=0, labelspacing=0.5)
#     axs.set_title(plot_desc)

# display(fig)

# fig.tight_layout()
# fig.savefig("plots/"+ exp_desc +".pdf")
