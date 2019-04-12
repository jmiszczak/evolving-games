import networkx as nx
import random as rnd
import numpy as np

# fix the random seed
#rnd.seed(19680801)


# chain initialization
def random_spin_chain(dim: int):
    # create the graph
    # spin_chain = nx.Graph()
    # for node in range(dim):
    #     spin_chain.add_node(node)
    # for node in range(dim-1):
    #     spin_chain.add_edge(node, node+1)

    spin_chain = nx.path_graph(dim)
    # initialize with random spins
    for node in spin_chain.nodes:
        spin_chain.nodes[node]['s'] = rnd.choice([-1, 1])

    return spin_chain


# update rule for the Sznajd model
def update_spin_sznajd(spin_chain, node):
    dim = len(spin_chain)
    # print(spin_chain.nodes)
    # print(node)
    if 0 < node < dim-2:
        if spin_chain.nodes[node]['s'] * spin_chain.nodes[node+1]['s'] == 1:
            spin_chain.node[node-1]['s'] = spin_chain.nodes[node]['s']
            spin_chain.node[node+2]['s'] = spin_chain.nodes[node]['s']
        else:
            spin_chain.node[node-1]['s'] = spin_chain.nodes[node+1]['s']
            spin_chain.node[node+2]['s'] = spin_chain.nodes[node]['s']
    return spin_chain


# main functionality
def main():
    # simulation steps
    steps = 100

    # chain length
    chain_dim = 100

    # tables with the results
    spin_state = list()
    mean_value = list()

    # initialize the chain
    spin_chain = random_spin_chain(chain_dim)
    spin_state.append(np.array([spin_chain.nodes[node]['s'] for node in spin_chain.nodes]))
    mean_value.append(np.mean(spin_state[-1]))

    # run the MC update on the nodes
    for st in range(steps):
        spin_chain = update_spin_sznajd(spin_chain, rnd.choice(list(spin_chain.nodes)))
        spin_state.append(np.array([spin_chain.nodes[node]['s'] for node in spin_chain.nodes]))
        mean_value.append(np.mean(spin_state[-1]))

    return (spin_state, mean_value)

if __name__ == '__main__':
    ret = main()
    print(ret[1])
