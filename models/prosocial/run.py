import networkx as nx
import random as rnd
import numpy as np


# random seed
# rnd.seed(42)


# initial strategies distributed with equal probability
def init_rnd_strategies(g: nx.Graph):
    for node in g.nodes:
        g.nodes[node]['s'] = rnd.choice(['C', 'D'])
        # g.nodes[node]['s'] = rnd.choice([1, 0]) # can be used instead


# payoffs initialization
def init_payoff(g: nx.Graph):
    for node in g.nodes:
        g.nodes[node]['v'] = 0


# payoff evaluation
def update_payoffs(g: nx.Graph, reward, temptation):
    for n in g.nodes:
        for neigh in nx.neighbors(g, n):
            if g.nodes[n]['s'] == 'C':
                if g.nodes[neigh]['s'] == 'C':
                    g.nodes[n]['v'] = g.nodes[n]['v'] + reward
                    g.nodes[neigh]['v'] = g.nodes[neigh]['v'] + reward
                elif g.nodes[neigh]['s'] == 'D':
                    pass
            elif g.nodes[n]['s'] == 'D':
                if g.nodes[neigh]['s'] == 'D':
                    pass
                elif g.nodes[neigh]['s'] == 'C':
                    g.nodes[n]['v'] = g.nodes[n]['v'] + temptation


# strategy updating
def update_node_strategy(tg: nx.Graph, n: object, rg: nx.Graph, model: str = 'S'):
    """
    Update the strategy of node `n` in the graph `tg` using information from the reference graph `rg`.
    :param tg: target graph
    :param n: target node
    :param rg: reference graph
    :param model: model of referencing
    :return: None
    """

    # parametres in formula (1) from Szolnoki and Perc, NJP, 15 (2013) 053010
    # scaling factors
    w_min = 0.1
    w_max = 1

    # K in the formula
    parameter_k = 1

    # accumulated payoff for players with both strategies
    payoff_coop = sum([tg.nodes[n]['v'] for n in tg.nodes if tg.nodes[n]['s'] == 'C'])
    payoff_deft = sum([tg.nodes[n]['v'] for n in tg.nodes if tg.nodes[n]['s'] == 'D'])

    # print(payoff_coop, " - ", payoff_deft)

    if model == 'S':
        if tg.nodes[n]['s'] == rg.nodes[n]['s']:
            wx = w_max
        else:
            wx = w_min
    else:
        print("[INFO] Model % not implemented" % model)
        pass

    flip_prob = wx/(1+np.exp(-1*(payoff_coop-payoff_deft)/parameter_k))
    rnd_neigh = rnd.choice(list(tg.neighbors(n)))
    tg.nodes[n]['s'] = rnd.choices([tg.nodes[n]['s'], tg.nodes[rnd_neigh]['s']], [1 - flip_prob, flip_prob])[0]


def play_game(turns):
    # size of the lattices
    dim1 = 20
    dim2 = 20

    # parameters of the game
    reward = 1
    temptation = 1.1

    # latices with initial data about the payoff and the strategies
    g1 = nx.grid_2d_graph(dim1, dim2, periodic=True)
    init_payoff(g1)
    init_rnd_strategies(g1)

    g2 = nx.grid_2d_graph(dim1, dim2, periodic=True)
    init_payoff(g2)
    init_rnd_strategies(g2)

    # all results
    final_payoffs_g1 = list()
    final_payoffs_g2 = list()

    final_strategies_g1 = list()
    final_strategies_g2 = list()

    # arrays for plotting values of payoffs
    vals_payoff_g1 = np.zeros([dim1, dim2])
    vals_payoff_g2 = np.zeros([dim1, dim2])

    vals_strategy_g1 = np.zeros([dim1, dim2])
    vals_strategy_g2 = np.zeros([dim1, dim2])

    for turn in range(turns):
        update_payoffs(g1, reward, temptation)
        update_payoffs(g2, reward, temptation)

        # read the values of the payoffs into
        for nd in g1.nodes:
            vals_payoff_g1[nd[0], nd[1]] = g1.nodes[nd]['v']
            vals_strategy_g1[nd[0], nd[1]] = 0 if g1.nodes[nd]['s'] == 'C' else 1

        for nd in g2.nodes:
            vals_payoff_g2[nd[0], nd[1]] = g2.nodes[nd]['v']
            vals_strategy_g2[nd[0], nd[1]] = 0 if g2.nodes[nd]['s'] == 'C' else 1

        final_payoffs_g1.append(vals_payoff_g1.copy())
        final_payoffs_g2.append(vals_payoff_g2.copy())

        final_strategies_g1.append(vals_strategy_g1.copy())
        final_strategies_g2.append(vals_strategy_g2.copy())

        for n in g1.nodes:
            update_node_strategy(g1, n, g2, model = 'S')

        for n in g2.nodes:
            update_node_strategy(g2, n, g1, model = 'S')

    np.savez("results/grid_payoffs.npz", g1 = final_payoffs_g1, g2 = final_payoffs_g2)
    np.savez("results/grid_strategies.npz", g1 = final_strategies_g1, g2 = final_strategies_g2)

# main function
play_game(1000)
