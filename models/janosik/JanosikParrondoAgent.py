import mesa

import numpy as np
import numpy.random as rnd

class JanosikParrondoAgent(mesa.Agent):
    """
    Implementation of an agent with initial amount of money and the policy for
    choosing games based on the Parrondo scheme. The goal of the agent is to
    decrease the inequality in the wealth distribution.

    Values of epsilon and M used in the Parrondo scheme are defined here.

    Each agent stores the history of played games. This can be used to include
    new deterministic policies for choosing games. 
    """
    def __init__(self, unique_id, model, position, policy, eps, boost):
        super().__init__(unique_id, model)
        self.capital = model.agent_init_capital+unique_id
        self.position = position
        self.eps = eps
        self.m = 3
        self.policy = policy
        self.game_hist = ['A', 'A', 'B', 'B']

        if boost == 'matthew' :
            self.boost_policy = [-1, -1]
        elif boost == 'antimatthew' :
            self.boost_policy = [1, 1]
        elif boost == 'strongmatthew' :
            self.boost_policy = [-1, -2]
        elif boost == 'strongantimatthew' :
            self.boost_policy = [2, 1]
        else :
            self.boost_policy = [1, 1]
        
        
    # single step of the evolution
    def step(self):
        """Execute one step"""
        self.move()
        if self.capital > 0:
            self.play()


    # movement of the agent
    def move(self):
        possible_steps = self.model.graph.get_neighbors(self.position)
        self.position = self.random.choice(possible_steps)
        self.model.graph.move_agent(self, self.position)

    def play(self):
        """Execute one step"""
        gain = 0
        
        # play against random opponent from the current cell
        cell_mates = self.model.graph.get_cell_list_contents([self.pos])
        
        if len(cell_mates) > 0 :
            other = self.random.choice(cell_mates)
        
            if other.capital > 1:
                # policy for choosing the game
                if self.policy == 'biasedB':
                    game = rnd.choice(['A', 'B'], p=[0.25, 0.75]) #  non-uniform random policy with preferred B
                elif self.policy == 'biasedA':
                    game = rnd.choice(['A', 'B'], p=[0.75, 0.25]) #  non-uniform random policy with preferred A
                elif self.policy == 'A':
                    game = 'A' # deterministic A
                elif self.policy == 'B':
                    game = 'B' # deterministic B
                elif self.policy == 'uniform':
                    game = rnd.choice(['A', 'B'], p=[0.5, 0.5]) #  uniform random policy
                elif self.policy == 'AB': # deterministic ABABAB...
                    if self.game_hist[-1] == 'A':
                        game = 'B'
                    elif self.game_hist[-1] == 'B':
                        game = 'A'
                    else:
                        game = 'A'
                elif self.policy == 'AABB': # deterministic AABBAABB...
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
                    if self.capital % self.m == 0:
                        # coin 2
                        gain = rnd.choice([1,-1], p=[0.10-self.eps, 0.90+self.eps])
                    else : 
                        # coin 3
                        gain = rnd.choice([1,-1], p=[0.75-self.eps, 0.25+self.eps])

                
                # Variant 1
                # interpret the gain in terms of the inequality reduction
                # this simulates the Matthew effect
                
                # winning means that the effect is reduced
                janosik_value = np.sign(self.capital - other.capital)
                if gain == 1:
                    self.capital -= janosik_value*self.boost_policy[0]
                    other.capital += janosik_value*self.boost_policy[0]
                        
                # loosing means that the effect is boosted
                elif gain == -1:
                    self.capital += janosik_value*self.boost_policy[1]
                    other.capital -= janosik_value*self.boost_policy[1]
      
