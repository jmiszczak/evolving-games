import mesa

class AxelrodAgent(mesa.Agent):
    """An agent."""

    def __init__(self, model):
        # Pass the parameters to the parent class.
        super().__init__(model)

        # Create the agent's variable and set the initial values.
        self.wealth = 1

    def step(self):
        # select a random agent
        other_agent = self.random.choice(self.model.agents)
        if other_agent is not None:
            other_agent.wealth += 1
            self.wealth -= 1
        print(f"Hi, I am an agent, you can call me {str(self.unique_id)}.")
