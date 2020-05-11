import mesa
import mesa.time as mt
import mesa.space as ms
import mesa.datacollection as md

import numpy.random as rnd

def defectors_rate(model):
    """
 
    Parameters
    ----------
    model : mesa.Model
        Mesa model representeing the game.

    Returns
    -------
    float
        Fraction of defectors among the agents of the model.

    """
    agents_strategies = [agent.strategy for agent in model.schedule.agents]
    agents_count = model.num_agents
    return sum(map(lambda x: 1 if x == "D" else 0, agents_strategies))/agents_count

class PDAgent(mesa.Agent):
    """An agent with initial amount of money"""
    def __init__(self, unique_id, model, temptation):
        super().__init__(unique_id, model)
        # agnet specific initialization
        self.strategy = rnd.choice(["C", "D"])
        self.wealth = 0
        self.temptation = temptation
        #print(self.strategy)

    # single step of the evolution
    # consists of a single game with a selected neighbour
    def step(self):
        """Execute one step"""
        self.move()
        if self.strategy in ["C", "D"]:
            self.play_pd_game()
            self.update_strategy()
        else :
           pass

    def play_pd_game(self):
        """
        Implementation of the prisoner's dilemma.

        Returns
        -------
        None.

        """
        neighs = self.model.grid.get_neighbors(self.pos, moore=False)
        if len(neighs) > 0 :
            other = self.random.choice(neighs)
            s0 = self.strategy          
            s1 = other.strategy
            payoff = []
            
            if s0 == s1:
                if s0 == 'D': # s1 =='D'
                    payoff = [0, 0]
                else: # s1 == s2 == 'C'
                    payoff = [1, 1]
            else:
                if s0 == 'D':
                    payoff = [1+self.temptation, 0]
                else: # s0 == 'C'
                    payoff = [0, 1+self.temptation]
            
            other.wealth += payoff[1]
            self.wealth += payoff[0]

    def update_strategy(self):
        neighs = self.model.grid.get_neighbors(self.pos, moore=False)
        # print("mates", mates)
        if len(neighs) > 0 :
            other = self.random.choice(neighs)
            w0 = self.wealth
            w1 = other.wealth
            payoff = []
            
            if w0 > self.model.temptation+w1 :            
                other.strategy = self.strategy
            elif w1 > 2*self.model.temptation+w0 :
                self.strategy = other.strategy
            else:
                pass    

    # movement of the agent -- not implemented yet
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

class PDGridModel(mesa.Model):
    def __init__(self, N, width, height, temptation):
        self.num_agents = N
        self.running = True
        self.grid = ms.MultiGrid(width, height, True)
        self.schedule = mt.RandomActivation(self)
        self.temptation = temptation

        # create and add agents
        for i in range(self.num_agents):
            # create an agent
            a = PDAgent(i, self, temptation)
            # add it to the scheduler
            self.schedule.add(a)
            # assign it to a location
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x,y))

        # add data collector
        self.datacollector = md.DataCollector(
            model_reporters = {"Defectors_rate": defectors_rate},
            agent_reporters = {"Strategy": "strategy"}
            )

    def step(self):
        """Execute one step for all agents"""
        self.datacollector.collect(self)
        self.schedule.step()
