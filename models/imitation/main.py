from pd_game import *

from sys import argv, stderr
from os import listdir

from functools import partial
from multiprocessing import Pool, cpu_count
from pathlib import Path

# count the number of nodes in population 's' in the graph 'g'
# we assume that the strategy is stored in 's' attribute of the node
def count(g, s):
    return len([g.nodes[n] for n in g.nodes if g.nodes[n]['s'] == s])

# NOTE: fixed random seed
#rnd.seed(42)

# implementation of the single experiment
# returns a list of agents in populations 'C' and 'D' 
def pd_run(g, r, t, ex_steps, **kwargs):

    # result - number of nodes in both populations
    res = list()

    # initialize the state
    g = pd_init_strategy(g)
    g = pd_init_payoff(g)

    # values in the 0th step
    res.append([count(g,'C'), count(g, 'D')])

    # run the game
    for k in range(1, ex_steps):
        g = pd_play(g, r, t)
        res.append([count(g, 'C'), count(g, 'D')])

    return res

def ex_run(ex_name, run_no):
    savez_dict = dict()
    run_number = '{:05d}'.format(run_no)
    run_name = '{}/{}'.format(ex_name, run_number)
    savez_dict[run_number] = pd_run(g, r, t, ex_steps)
    np.savez(run_name, **savez_dict)
    print('[INFO]',  run_name, 'saved.', file=stderr)


if __name__ == '__main__':
    
    #-----------------------------
    # parameters of the experiment
    #-----------------------------
    # name
    g_type = 'grid_2d_p'
    # size of the graph
    dim1, dim2 = 30, 30
    # form of the graph
    g = nx.grid_2d_graph(dim1, dim2, periodic=True)
    # number or steps
    ex_steps = 200
    # default number of experiments
    ex_count = 10
  
    #-----------------------
    # parameters of the game
    #-----------------------
    # PD parameters
    # reward
    r = 1
    # temptation
    t = r + 0.2
    pd_param = "t-r" + str(round(t-r,1))
    
    # experiment identification - graph info and graph type
    g_info = str(dim1)+"x"+str(dim2)
    ex_name = '{}_{}_{}'.format(g_type, g_info, pd_param)

    # selecting the action to run
    cmd = ''
    cmd_info = ''

    if len(argv)<2:
        print("[ERROR] Please select 'run', 'prun' or 'plot' as the action (first argument).")
        exit(-1)
    else:
        # chose the action
        cmd = argv[1] # can be 'run' or 'plot'

    if cmd == 'run':
        cmd_info = 'Executing'
    elif cmd == 'prun':
        cmd_info = 'Executing in parallel'
    elif cmd == 'plot':
        cmd_info = 'Plotting'
   
    # construct the range for experiments
    # can be used for running on grid or adding new data
    if len(argv) == 2:
        if cmd == 'plot':
            print("[INFO]", cmd_info, len(listdir(ex_name)), "experiments.", file=stderr)
        else:   
            print("[INFO]", cmd_info, ex_count, "experiments.", file=stderr)
        ex_range = range(ex_count)
        ex_range_name = "{:05d}-{:05d}".format(0,ex_count-1)
    elif len(argv) == 4: # for grid/adding data
        rs, re = int(argv[2]), int(argv[3])
        print("[INFO]", cmd_info, "experiments in range {:05d}-{:05d}".format(rs, re), file=stderr)
        ex_range = range(rs, re)
        ex_range_name = "{:05d}-{:05d}".format(rs,re)
    else:
        print("[INFO]", cmd_info, "with fallback to the default range.", file=stderr)
        ex_range = range(ex_count)
        ex_range_name = "{:05d}-{:05d}".format(0,ex_count)


    Path(ex_name).mkdir(exist_ok=True)
    
    if cmd == 'run':
        for k in ex_range:
            ex_run(ex_name, k)

    if cmd == 'prun':
        p = Pool(cpu_count())
        ex_run_p = partial(ex_run, ex_name)
        p.map(ex_run_p, ex_range)

    if cmd == 'plot':
        mean_coop = np.zeros(ex_steps)
        mean_defe = np.zeros(ex_steps)

        # read data from the file using the same formating
        for f_name in listdir(ex_name):
            key = f_name.split('.')[0]
            data = np.load(ex_name + "/" + key + '.npz')[key]
            mean_coop += data[:,0]
            mean_defe += data[:,1]

        mean_coop = mean_coop/len(listdir(ex_name))
        mean_defe = mean_defe/len(listdir(ex_name))

        fig = plt.figure()
        plt.plot(mean_coop, color='green', linestyle='solid')
        plt.plot(mean_defe, color='red', linestyle='dashed')
        plt.show()
