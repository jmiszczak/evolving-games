import mesa 
import mesa.time as mt
import numpy.random as rnd

class ParrondoAgent(mesa.Agent):
    """
    An agent with initial amount of money. Values of epsilon and M are defined
    here.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = 100
        self.eps = 0.055
        self.m = 3

    def step(self):
        """Execute one step"""
        gain = 0
        # play against random opponent
        other = self.random.choice(self.model.schedule.agents)
        
        # policy for choosing the game
        #game = rnd.choice(['A', 'B'], p=[0.25, 0.75]) #  non-uniform random policy
        game = rnd.choice(['A', 'B'], p=[0.5, 0.5]) #  uniform random policy
        
        # calculation of the gain
        if game == 'A':
            # coin 1
            gain = rnd.choice([1,-1],p=[0.5-self.eps, 0.5+self.eps])
        elif game == 'B':
            if self.wealth % self.m == 0:
                # coin 2
                gain = rnd.choice([1,-1], p=[0.10-self.eps, 0.90+self.eps])
            else : 
                # coin 3
                gain = rnd.choice([1,-1], p=[0.75-self.eps, 0.25+self.eps])

        other.wealth += gain 
        self.wealth -= gain

class ParrondoModel(mesa.Model):
    def __init__(self, N):
        self.num_agents = N
        self.schedule = mt.RandomActivation(self)
        # create and add agents
        for i in range(self.num_agents):
            a = ParrondoAgent(i, self)
            self.schedule.add(a)

    def step(self):
        """Execute one step for all agents"""
        self.schedule.step()
