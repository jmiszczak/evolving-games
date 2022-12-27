using Agents

# define agent type
@agent MoneyGridAgent GridAgent{2} begin
    wealth::Int
end

# describe evolution of the agent
function agent_step!(agent, model)
    if agent.wealth == 0
        return
    else
        r_agent = random_agent(model)
        agent.wealth -= 1
        r_agent.wealth += 1
    end
end

# create the world = build a model and add agents
function create_world(; dim = 100, numagents = 100, initwealth = 1)
    # build a grid with given dimension
    grid_space = GridSpace((dim, dim); periodic = false)
    # create a model
    abm_model = ABM(MoneyGridAgent, grid_space; scheduler = Schedulers.randomly)
    # add agents
    for n in 1:numagents
        agent = MoneyGridAgent(n, (1,1), initwealth)
        add_agent!(agent, abm_model)
    end
    return abm_model
end

world = create_world(dim = 100, numagents = 100, initwealth = 10)
adata = [:wealth]
data, _ = run!(world, agent_step!, 9; adata)