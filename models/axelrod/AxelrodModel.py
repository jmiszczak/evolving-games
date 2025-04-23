import mesa

from AxelrodAgent import AxelrodAgent

class AxelrodModel(mesa.Model):
    """A model with some number of agents."""

    def __init__(self, n, seed=None):
        super().__init__(seed=seed)
        self.num_agents = n
        # Create agents
        for _ in range(self.num_agents):
            # Note: no need to add the agent to the schedule
            a = AxelrodAgent(self)

    def step(self):
        """Advance the model by one step."""

        # This function psuedo-randomly reorders the list of agent objects and
        # then iterates through calling the function passed in as the parameter
        self.agents.shuffle_do("step")
        # self.agents.do("step")

    def print_agents(self):
        for a in self.agents:
            print(a.unique_id)