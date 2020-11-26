import mesa

import numpy as np
import numpy.random as rnd

class JanosikAgent(mesa.Agent):
    """
    Implementation of an agent with initial amount of money and the policy for
    reduction the ineqaulity in the capital distribution. 

    The game played by the agen has only one parameter, which is interpreter
    as a bias toward wining.
    
    The boost is used to change the strength of the interpreteation according 
    the Matthew effect.
    """
    def __init__(self, unique_id, model, position, eps, boost):
        super().__init__(unique_id, model)
        self.capital = model.agent_init_capital+unique_id
        self.position = position
        self.eps = eps

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
        if self.capital > 1:
            self.play()


    # movement of the agent
    def move(self):
        possible_steps = self.model.graph.get_neighbors(self.position)
        self.position = self.random.choice(possible_steps)
        self.model.graph.move_agent(self, self.position)

    # implementation of a single step
    def play(self):
        """
        Execute one step of the scheme. This consists of playing a biased coin
        flip game with a randomly selected agent from the current cell, and 
        modifying the capital of both players.
        """
        gain = 0
        
        # play against random opponent from the current cell
        cell_mates = self.model.graph.get_cell_list_contents([self.pos])
        
        if len(cell_mates) > 0 :
            other = self.random.choice(cell_mates)
            
            if other.capital > 1:
                gain = rnd.choice([1,-1], p=[0.5-self.eps, 0.5+self.eps])               
                
                # interpret the gain in terms of the inequality reduction
                # this simulates the Matthew effect
                
                # winning means that the effect is reduced
                if gain == 1:
                    self.capital -= np.sign(self.capital - other.capital)*self.boost_policy[0]
                    other.capital += np.sign(self.capital - other.capital)*self.boost_policy[0]
                        
                # loosing means that the effect is boosted
                elif gain == -1:
                    self.capital += np.sign(self.capital - other.capital)*self.boost_policy[1]
                    other.capital -= np.sign(self.capital - other.capital)*self.boost_policy[1]
               
                
            