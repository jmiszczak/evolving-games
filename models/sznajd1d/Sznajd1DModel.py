import networkx as nx
import random as rnd

import mesa
import mesa.space as ms
import mesa.time as mt
import mesa.datacollection as md

def vote_result(model):
    opinions = [agent.opinion for agent in model.schedule.agents]
    return sum(opinions)/model.num_agents

def individual_votes(model):
    return [agent.opinion for agent in model.schedule.agents]

class Sznajd1DAgent(mesa.Agent):
    # 
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.opinion = self.random.choice([-1,1])
    
    # update the opinion
    def step(self):
        self.update_opinion()

    def update_opinion(self):
        # select a neighbor
        rn = rnd.choice(list(self.model.grid.get_neighbors(self.unique_id)))
        # get its opinion
        rn_op = self.model.grid.get_cell_list_contents([rn])[0].opinion
        # update opinions
        if self.opinion*rn_op == 1:
            print("OK")
        else:
            print("Agrrrr")




class Sznajd1DModel(mesa.Model):
    def __init__(self, width):
        self.running = True
        self.num_agents = width
        self.schedule = mt.RandomActivation(self)
        self.grid = ms.NetworkGrid(nx.grid_graph(dim=[self.num_agents], periodic=False))
        self.x = [(x) for x in range(self.num_agents)]

        self.datacollector = md.DataCollector(
                model_reporters = {'Average opinion' : vote_result, 'Agent opinions': individual_votes },
                agent_reporters = {'Opinion': 'opinion'}
                )

        for uid in range(self.num_agents):
            a = Sznajd1DAgent(uid, self)
            self.schedule.add(a)
            self.grid.place_agent(a, self.x[uid])

    # simulation step
    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
