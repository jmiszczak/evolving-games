from SznajdModel import SznajdModel

width = 100
height = 1
no_agents = width*height

model = SznajdModel(no_agents, width, height)

model.step()
