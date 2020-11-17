import mesa
import mesa.time as mt
import mesa.space as ms
import mesa.datacollection as md

import numpy.random as rnd
import networkx as nx

import sys
sys.path.append('..')

import indicators

from ParrondoAgent import ParrondoAgent

class ParrondoGraphModel(mesa.Model):
    
    def __init__(self, num_agents, graph_spec, init_wealth, default_policy, default_eps, default_boost):
        self.num_agents = num_agents
        self.agent_init_wealth = init_wealth
        self.running = True
        
        if type(graph_spec) == nx.classes.graph.Graph:
            self.graph = ms.NetworkGrid(graph_spec)
        elif type(graph_spec) == str:
            self.graph = ms.NetworkGrid(nx.readwrite.read_gexf(graph_spec))
        self.schedule = mt.RandomActivation(self)

        # create and add agents 
        for aid in range(self.num_agents):
            # select a graph node
            position = list(self.graph.G.nodes)[rnd.choice(range(len(list(self.graph.G.nodes))))]
            # create an agent
            agent = ParrondoAgent(aid, self, position, default_policy, default_eps, default_boost)
            # add it to the scheduler
            self.schedule.add(agent)
            # assign it to a location
            self.graph.place_agent(agent, position)

        # add data collector
        self.datacollector = md.DataCollector(
            model_reporters = {"Gini index": indicators.gini_index, 
                               "Total wealth": indicators.total_wealth, 
                               "Mean wealth": indicators.mean_wealth,
                               "Median wealth": indicators.median_wealth,
                               },
            agent_reporters = {"Wealth": "wealth"}
            )

    def step(self):
        """Execute one step for all agents"""
        self.datacollector.collect(self)
        self.schedule.step()
