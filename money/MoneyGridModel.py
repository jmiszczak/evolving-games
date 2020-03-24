import mesa
import mesa.time as mt
import mesa.space as ms
import mesa.datacollection as md

import numpy.random as rnd

def gini(model):
    agent_wealths = [agent.wealth for agent in model.schedule.agents]
    x = sorted(agent_wealths)
    N = model.num_agents
    B = sum( xi * (N-i) for i,xi in enumerate(x) ) / (N*sum(x))
    return (1 + (1/N) - 2*B)

class MoneyAgent(mesa.Agent):
    """An agent with initial amount of money"""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = 1

    # single step of the evolution
    def step(self):
        """Execute one step"""
        self.move()
        if self.wealth == 0 :
            pass
        else :
           self.give_money()

    # movement of the agent
    def move(self):
        # each agent knows about the model
        possible_steps = self.model.grid.get_neighborhood(
                self.pos,
                moore = True, 
                include_center = False
            )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def give_money(self):
        cell_mates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cell_mates) > 0 :
            other = self.random.choice(cell_mates)
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

        # add data collector
        self.datacollector = md.DataCollector(
            model_reporters = {"Gini": gini},
            agent_reporters = {"Wealth": "wealth"}
            )

    def step(self):
        """Execute one step for all agents"""
        self.datacollector.collect(self)
        self.schedule.step()
