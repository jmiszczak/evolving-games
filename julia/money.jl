using Agents

mutable struct MoneyAgent <: AbstractAgent
    id::Int
    wealth::Int
end

function agent_step!(agent, model)
    if agent.wealth == 0
        return # do nothing
    else
        ragent = random_agent(model)
        agent.wealth -= 1
        ragent.wealth += 1
    end
end

function create_model(; numagents = 100, initwealth = 1)
    model = AgentBasedModel(
        MoneyAgent;
        scheduler = Schedulers.Randomly()
    )
    for _ in 1:numagents
        add_agent!(model,initwealth) # initialize wealth to initwealth
    end 
    return model
end

adata = [:wealth]

steps = 1
agents = 500

model = create_model(numagents = agents)

data, _ = run!(model, agent_step!, steps; adata)
data[(end-20):end, :]