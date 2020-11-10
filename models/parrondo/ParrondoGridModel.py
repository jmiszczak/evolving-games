import mesa
import mesa.time as mt
import mesa.space as ms
import mesa.datacollection as md

import numpy.random as rnd

import sys
sys.path.append('../')

import indicators


class ParrondoAgent(mesa.Agent):
    """
    An agent with initial amount of money. Values of epsilon and M are defined
    here.
    """
    def __init__(self, unique_id, model, policy, eps):
        super().__init__(unique_id, model)
        self.wealth = rnd.randint(model.agent_init_wealth/2,3*model.agent_init_wealth/2) 
        self.eps = eps
        self.m = 3
        self.policy = policy
        
    # single step of the evolution
    def step(self):
        """Execute one step"""
        self.move()
        if self.wealth > 0:
            self.play()


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

    def play(self):
        """Execute one step"""
        gain = 0
        
        # play against random opponent from the current cell
        cell_mates = self.model.grid.get_cell_list_contents([self.pos])
        
        if len(cell_mates) > 0 :
            other = self.random.choice(cell_mates)
        
            # policy for choosing the game
            if self.policy == 'biased-towards-B':
                game = rnd.choice(['A', 'B'], p=[0.25, 0.75]) #  non-uniform random policy with prefered B
            elif self.policy == 'biased-towards-A':
                game = rnd.choice(['A', 'B'], p=[0.75, 0.25]) #  non-uniform random policy with prefered A
            elif self.policy == 'only-A':
                game = 'A' # deterministic with prefered A
            elif self.policy == 'only-B':
                game = 'B' # deterministic with prefered B
            else: # default policy is uniform
                game = rnd.choice(['A', 'B'], p=[0.5, 0.5]) #  uniform random policy
            
            # calculation of the gain
            if game == 'A':
                # coin 1
                gain = rnd.choice([1,-1], p=[0.5-self.eps, 0.5+self.eps])
            elif game == 'B':
                if other.wealth % self.m == 0:
                    # coin 2
                    gain = rnd.choice([1,-1], p=[0.10-self.eps, 0.90+self.eps])
                else : 
                    # coin 3
                    gain = rnd.choice([1,-1], p=[0.75-self.eps, 0.25+self.eps])
    
            self.wealth -= gain
            other.wealth += gain
            
        else :
            self.move()
            self.play()

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
            model_reporters = {"Gini": indicators.gini},
            agent_reporters = {"Wealth": "wealth"}
            )

    def step(self):
        """Execute one step for all agents"""
        self.datacollector.collect(self)
        self.schedule.step()
