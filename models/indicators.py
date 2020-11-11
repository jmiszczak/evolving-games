#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 10:04:57 2020

@author: jam
"""
def gini(model):
    agent_wealths = sorted([agent.wealth for agent in model.schedule.agents])
    N = model.num_agents
    # return sum([(2*(i+1)-N-1)*x for i,x in enumerate(agent_wealths) ])/(N*sum(agent_wealths))
    
    return sum([abs(xi-xj) for xi in agent_wealths for xj in agent_wealths ]) /(2*N*sum(agent_wealths))