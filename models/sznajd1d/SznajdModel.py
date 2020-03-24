import mesa
import mesa.space as ms
import mesa.time as mt
import mesa.datacollection as md

def average_opinion(model):
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
        mates_pos = self.model.grid.get_neighborhood(
                self.pos, 
                moore=True,
                include_center=False)
        mates = self.model.grid.get_cell_list_contents(mates_pos) 
        if len(mates) == 2:
            if self.opinion == mates[0].opinion:
                mates[1].opinion = self.opinion
            elif self.opinion == mates[1].opinion:
                mates[0].opinion = self.opinion
            else :
                self.opinion = mates[0].opinion
        
        # print("UID:", self.unique_id, mates)


class SznajdModel(mesa.Model):
    def __init__(self, N, width, height):
        self.num_agents = N
        self.schedule = mt.RandomActivation(self)
        self.grid = ms.MultiGrid(width, height, False)
        self.xy = [(x,y) for x in range(width) for y in range(height)]

        self.datacollector = md.DataCollector(
                model_reporters = {'Average opinion' : average_opinion},
                agent_reporters = {'Opinion': 'opinion'}
                )

        for uid in range(self.num_agents):
            a = SznajdAgent(uid, self)
            self.schedule.add(a)
            self.grid.place_agent(a, self.xy[uid])

    # simulation step
    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
