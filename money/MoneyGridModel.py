import mesa
import mesa.time as mt
import mesa.space as ms

import numpy.random as rnd

class MoneyAgent(mesa.Agent):
    """An agent with initial amount of money"""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = 1

    def step(self):
        """Execute one step"""
        if self.wealth == 0 :
            pass
        else :
            other = self.random.choice(self.model.schedule.agents)
            other.wealth += 1
            self.wealth -= 1

class MoneyGridModel(mesa.Model):
    def __init__(self, N, width, height):
        self.num_agents = N
        self.grid = ms.MultiGrid(width, height, True)
        self.schedule = mt.RandomActivation(self)

        # create and add agents
        for i in range(self.num_agents):
            # create an agent
            a = MoneyAgent(i, self)
            # add it to the scheduler
            self.schedule.add(a)
            # assign it to a location
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x,y))

    def step(self):
        """Execute one step for all agents"""
        self.schedule.step()
