using Distributed

addprocs(6)

@everywhere begin
  using Agents
  using Random
  using CairoMakie
end

#
# general variables 
#
# space to run the model (eg. 2D grid)
size = 16
dims = (size, size)

# number of agents
numagents = size*size
# number of steps
numsteps = 64
# random seed
seed = 452

#
# agent
#
@everywhere @agent PGGAgent{} GridAgent{2} begin
  # income in the last round
  income::Real
  # contrib: 0 => freerider, 1 => cooperator
  contrib::Int
end

#
# agent has 
# - to chooose its neighbours (von Neuman or Moore neigbourhood)
# - play PGG game
# - imitate a strategy using Fermi-Dirac function
#
@everywhere function agent_step!(agent, model)
  total_contrib = 0
  num_neighbors = 0
  for neighbor in nearby_agents(agent, model)
    total_contrib += neighbor.contrib 
    num_neighbors += 1
  end
  agent.income = model.synergy_r*(total_contrib + agent.contrib)/(num_neighbors + 1) - agent.contrib
  random_neigbour = random_nearby_agent(agent, model)
  # if random_neigbour.income > agent.income
  #   agent.contrib = random_neigbour.contrib
  # else
  #   random_neigbour.contrib = agent.contrib 
  # end

  imit_prob = 1/(1+exp((random_neigbour.income - agent.income)/model.noise_k))
  println(imit_prob)
  if rand() < imit_prob
    agent.contrib = random_neigbour.contrib
  end
end

#
# model
# - contains info about the interaction neighborhood

@everywhere function setup_model(;
    numagents = 16,
    dims = (16,16),
    synergy_r = 3.0,
    noise_k = 0.5,
    seed = 23182
  )
  # some 
  rng = MersenneTwister(seed)
  scheduler = Schedulers.randomly
  space = GridSpaceSingle(dims; periodic = true)
  properties = Dict(
    :synergy_r => synergy_r,
    :noise_k => noise_k
  ) 
  
  # create a model
  model = ABM(
    PGGAgent, 
    space;
    properties,
    scheduler
  )

  # create agents
  for n in 1:numagents
    agent = PGGAgent(n, (1,1), 0, rand(rng, (0,1)))
    add_agent_single!(agent, model)
  end

  return model

end

#
# simulation
#
#
model = setup_model(numagents=numagents, dims=dims, seed=seed, synergy_r=3.0, noise_k = 0.5)

# calculate number of cooperators
function count_cooperators(model)
  
end


groupcolor(a) = a.contrib == 0 ? :red : :green
groupmarker(a) = a.contrib == 0 ? :circle : :rect
figure, _ = abmplot(model; ac = groupcolor, am = groupmarker, as = 20)
figure # returning the figure displays it

step!(model, agent_step!, 3)

abmvideo(
    "pgg-grid.mp4", model, agent_step!;
    ac = groupcolor, am = groupmarker, as = 20,
    framerate = 4, frames = numsteps,
    title = "Basic Public Goods Game"
)