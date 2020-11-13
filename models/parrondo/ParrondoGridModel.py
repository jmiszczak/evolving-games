import mesa
import mesa.time as mt
import mesa.space as ms
import mesa.datacollection as md

import sys
sys.path.append('../')

import indicators

from ParrondoAgent import ParrondoAgent

class ParrondoGridModel(mesa.Model):
    
    def __init__(self, N, width, height, init_wealth, default_policy, default_eps):
        self.num_agents = N
        self.agent_init_wealth = init_wealth
        
        self.running = True
        self.grid = ms.MultiGrid(width, height, True)
        self.schedule = mt.RandomActivation(self)

        # create and add agents
        for i in range(self.num_agents):
            # create an agent
            a = ParrondoAgent(i, self, default_policy, default_eps)
            # add it to the scheduler
            self.schedule.add(a)
            # assign it to a location
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x,y))

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
