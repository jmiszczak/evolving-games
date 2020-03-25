import networkx as nx

import mesa
import mesa.space as ms
import mesa.time as mt
import mesa.datacollection as md

def vote_result(model):
    opinions = [agent.opinion for agent in model.schedule.agents]
    return sum(opinions)/model.num_agents

class SznajdAgent(mesa.Agent):
    # 
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.opinion = self.random.choice([-1,1])
    
    # update of the opinion
    def step(self):
        self.update_opinion()

    def update_opinion(self):
        mates_pos = self.model.grid.get_neighbors(
                self.unique_id, 
                include_center=False)
        mates = self.model.grid.get_cell_list_contents(mates_pos) 

        # only two opinion are taken into account
        if len(mates) == 2:
            if self.opinion == mates[0].opinion:
                mates[1].opinion = self.opinion
            elif self.opinion == mates[1].opinion:
                mates[0].opinion = self.opinion
            else :
                self.opinion = mates[0].opinion
        else :
            raise BaseException("wrong number of neighbors")


class SznajdModel(mesa.Model):
    def __init__(self, width, height):
        self.num_agents = width*height
        self.schedule = mt.RandomActivation(self)
        self.grid = ms.NetworkGrid(nx.grid_graph(dim=[self.num_agents], periodic=True))
        self.x = [(x) for x in range(self.num_agents)]

        self.datacollector = md.DataCollector(
                model_reporters = {'Average opinion' : vote_result},
                agent_reporters = {'Opinion': 'opinion'}
                )

        for uid in range(self.num_agents):
            a = SznajdAgent(uid, self)
            self.schedule.add(a)
            self.grid.place_agent(a, self.x[uid])

    # simulation step
    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
