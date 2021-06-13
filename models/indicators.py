#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 10:04:57 2020

@author: jam
"""

import numpy as np

def gini_index(model):
    agents_capital = sorted([agent.capital for agent in model.schedule.agents])
    return sum([abs(xi-xj) for xi in agents_capital for xj in agents_capital ]) /(2*model.num_agents*sum(agents_capital))


def hoover_index(model):
    agents_capital = [agent.capital for agent in model.schedule.agents]
    mean_capital = (1/model.num_agents)*sum(agents_capital)
    
    return (0.5/sum(agents_capital))*sum([abs(xi - mean_capital) for xi in agents_capital])



def total_capital(model):
    return sum([agent.capital for agent in model.schedule.agents])


def mean_capital(model):
    return np.mean([agent.capital for agent in model.schedule.agents])


def median_capital(model):
    return np.median([agent.capital for agent in model.schedule.agents])


def min_capital(model):
    return min([agent.capital for agent in model.schedule.agents])


def max_capital(model):
    return max([agent.capital for agent in model.schedule.agents])