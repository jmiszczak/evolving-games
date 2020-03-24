import networkx as nx
import random as rnd

# --------------------------------------------------------------------------
# Implementation of functionality required to run Prisoner's Dilemma game on
# a graph. Provides methods for initializing strategies and payoffs,
# for evaluating payoffs, and for updating strategies.
#
# A single run of a game on a graph is executed using pd_play.
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Initialization functions.
# ---------------------------------------------------------------------------

#
# initial strategies distributed with equal probability
def pd_init_strategy(g, strats = ['C', 'D']):
    for n in g.nodes:
        g.nodes[n]['s'] = rnd.choice(strats)
        
    return g


# payoffs initialization
def pd_init_payoff(g, init_v = 0):
    for n in g.nodes:
        g.nodes[n]['v'] = init_v

    return g


# ---------------------------------------------------------------------------
# Evaluation of the payoff function.
# ---------------------------------------------------------------------------

# payoff function for two payers n1 and n2
def pd_payoff(g, n1, n2, r, t):
    pf = [0, 0]
    s1 = g.node[n1]['s']
    s2 = g.node[n2]['s']
    if s1 == s2:
        if s1 == 'D': # s2 =='D'
            pf = [0, 0]
        else: # s1 == s2 == 'C'
            pf = [r, r]
    else:
        if s1 == 'D':
            pf = [t, 0]
        else: # s1 == 'C'
            pf = [0, t]
    return pf


# accumulated payoff for player n playing with all neighbors
def pd_local_payoff(g, n, r, t):
    lpf = 0
    for x in g.neighbors(n):
        lpf += pd_payoff(g, n, x, r, t)[0]

    return lpf


# update payoff for all players by playing with all neighbors
def pd_update_payoff(g, r, t):
    for n in g.nodes:
        g.nodes[n]['v'] =+ pd_local_payoff(g, n, r, t)

    return g


# ---------------------------------------------------------------------------
# Imitation process based on the accumulated payoff.
# ---------------------------------------------------------------------------

def pd_update_strategy(g, r, t):
    for n in g.nodes:
        # select one of the neighbors
        rn = rnd.choice(list(nx.neighbors(g, n)))
        
        # check current the strategies of the selected neighbors and the node
        sn = g.nodes[n]['s']
        sr = g.nodes[rn]['s']
        
        # payoff difference
        pd = pd_local_payoff(g, rn, r, t) - pd_local_payoff(g, n, r, t)

        # calculate the imitating probability
        pim = pd/(t*max(g.degree(rn), g.degree(n))) if pd>0 else 0
       
        # update the strategy
        g.nodes[n]['s'] = rnd.choices([sr, sn], [pim, 1-pim])[0]

    return g

# ---------------------------------------------------------------------------
# Execution of the game on the given graph.
# ---------------------------------------------------------------------------

def pd_play(g = None, r = 1, t = 2, g0 = None):
    """

    :param g: graph describing connections between the players
    :param r: payoff for the cooperation strategy
    :param t: payoff for the defection vs cooperation strategy
    :param g0: graph describing potential connections between the players
    :return: grid describing the configuration after one step
    """

    # execute the game

    # update payoffs
    g = pd_update_payoff(g, r, t)
    # imitation process
    g = pd_update_strategy(g, r, t)

    return g
