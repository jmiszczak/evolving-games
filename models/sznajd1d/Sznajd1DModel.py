import networkx as nx

import mesa
import mesa.space as ms
import mesa.time as mt
import mesa.datacollection as md

def vote_result(model):
    opinions = [agent.opinion for agent in model.schedule.agents]
    return sum(opinions)/model.num_agents

class Sznajd1DAgent(mesa.Agent):
    # 
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.opinion = self.random.choice([-1,1])
    
    # update of the opinion
    def step(self):
        self.update_opinion()

    def update_opinion(self):
        # max position is equal to the number of agents
        max_pos = self.model.num_agents
        # assume period boundary conditions
        ng_pos = [(self.pos+i) % max_pos for i in [-2,-1,1,2]]
        # extract agents
        ng = self.model.grid.get_cell_list_contents(ng_pos) 

        # only two opinion are taken into account
        # but the opinion is set for three neighbors
        if len(ng) == 4:
            if self.opinion*ng[2].opinion == 1:
                ng[1].opinion = self.opinion
                ng[3].opinion = self.opinion
            elif self.opinion*ng[2].opinion == -1:
                ng[1].opinion = ng[2].opinion
                ng[3].opinion = self.opinion
        else :
            raise BaseException("wrong number of neighbors")


class Sznajd1DModel(mesa.Model):
    def __init__(self, width):
        self.running = True
        self.num_agents = width
        self.schedule = mt.RandomActivation(self)
        self.grid = ms.NetworkGrid(nx.grid_graph(dim=[self.num_agents], periodic=True))
        self.x = [(x) for x in range(self.num_agents)]

        self.datacollector = md.DataCollector(
                model_reporters = {'Average opinion' : vote_result},
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
