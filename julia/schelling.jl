using Agents
using InteractiveDynamics
using CairoMakie
using Statistics: mean

# agent type
mutable struct Schelling <: AbstractAgent
  id::Int
  pos::Tuple{Int,Int}
  group::Int
  happy::Bool
end

# initialize the model
function initialize(; N = 320, M = 20, min_to_be_happy = 3)
  space = GridSpace((M,M))
  scheduler = Schedulers.randomly
  properties = Dict(:min_to_be_happy => min_to_be_happy)
  model = AgentBasedModel(Schelling,
                        space;
                        properties,
                        scheduler)
  for n in 1:N
    agent = Schelling(n, (1,1), n < N/2 ? 1 : 2, false)
    add_agent_single!(agent, model)
  end
  return model
end

function agent_step!(agent, model)
  agent.happy && return

  nearby_same = 0
  for neighbor in nearby_agents(agent, model)
    if agent.group == neighbor.group
      nearby_same += 1
    end
  end

  if nearby_same >= model.min_to_be_happy
    agent.happy = true
  else
    move_agent_single!(agent, model)
  end

end

# function to terminate
#t(model, s) = s == 3

#
# evolution and plotting
#
model = initialize()
step!(model, agent_step!, 3)

# plot
groupcolor(agent) = agent.group == 1 ? :blue : :orange 
groupmarker(agent) = agent.group == 1 ? :circle : :rect
fig, _ = abmplot(model; ac = groupcolor, am = groupmarker, as = 10)
display(fig)

#
# evolve and agregate data 
#
model = initialize()
x(agent) = agent.pos[1]
# data to agregate
adata = [x, :happy, :group]
data, _ = run!(model, agent_step!, 500; adata);
data[1:10, :]

#
# interacive environement
#
# patameters
parange = Dict(:min_to_be_happy => 0:8)
# collected data
adata = [(:happy, sum), (:happy, mean)]
# model
model = initialize()
# evolution
adf, mdf = run!(model, agent_step!, 5; adata)
# labels
alabels = ["happy", "avg. x"]

figure, _ = abmexploration(model)

display(figure)