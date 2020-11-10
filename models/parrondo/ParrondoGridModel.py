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
    An agent with initial amount of money and the policy for choosin games.
    Values of epsilon and M used in the Parronodo scheme are defined here.
    """
    def __init__(self, unique_id, model, policy, eps):
        super().__init__(unique_id, model)
        self.wealth = model.agent_init_wealth*(unique_id+1)
        self.eps = eps
        self.m = 3
        self.policy = policy
        self.game_hist = ['A', 'A', 'B', 'B']
        
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
        
            if other.wealth > 1:
                # policy for choosing the game
                if self.policy == 'biasedB':
                    game = rnd.choice(['A', 'B'], p=[0.25, 0.75]) #  non-uniform random policy with preferred B
                elif self.policy == 'biasedA':
                    game = rnd.choice(['A', 'B'], p=[0.75, 0.25]) #  non-uniform random policy with preferred A
                elif self.policy == 'A':
                    game = 'A' # deterministic with prefered A
                elif self.policy == 'B':
                    game = 'B' # deterministic with prefered B
                elif self.policy == 'uniform': # default policy is uniform
                    game = rnd.choice(['A', 'B'], p=[0.5, 0.5]) #  uniform random policy
                elif self.policy == 'AB':
                    if self.game_hist[-1] == 'A':
                        game = 'B'
                    elif self.game_hist[-1] == 'B':
                        game = 'A'
                    else:
                        game = 'A'
                elif self.policy == 'AABB':
                    if self.game_hist[-1] == 'A':
                        if self.game_hist[-2] == 'A':
                            game = 'B'
                        else:
                            game = 'A'
                    if self.game_hist[-1] == 'B':
                        if self.game_hist[-2] == 'B':
                            game = 'A'
                        else:
                            game = 'B'
                
                self.game_hist.append(game)
                
                # calculation of the gain using three biased coins
                if game == 'A':
                    # coin 1
                    gain = rnd.choice([1,-1], p=[0.5-self.eps, 0.5+self.eps])
                elif game == 'B':
                    if self.wealth % self.m == 0:
                        # coin 2
                        gain = rnd.choice([1,-1], p=[0.10-self.eps, 0.90+self.eps])
                    else : 
                        # coin 3
                        gain = rnd.choice([1,-1], p=[0.75-self.eps, 0.25+self.eps])

                
                # interpret the gain in terms of the inequality reduction
                # this simulates the Matthew effect
                
                # winning means that the effect is reduced
                if gain == 1:
                    if self.wealth < other.wealth :
                        self.wealth += 1
                        other.wealth -= 1
                    elif self.wealth > other.wealth :
                        self.wealth -= 1
                        other.wealth += 1
                    else:
                        pass
                # loosing means that the effect is boosted
                elif gain == -1:
                    if self.wealth < other.wealth :
                        self.wealth -= 1
                        other.wealth += 1
                    elif self.wealth > other.wealth :
                        self.wealth += 1
                        other.wealth -= 1
                else:
                    pass
                
            else:
                pass
        else:
            pass            

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
            model_reporters = {"Gini index": indicators.gini},
            agent_reporters = {"Wealth": "wealth"}
            )

    def step(self):
        """Execute one step for all agents"""
        self.datacollector.collect(self)
        self.schedule.step()
