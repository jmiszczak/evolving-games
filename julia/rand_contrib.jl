using Agents

#
# general variables 
#
# space to run the model (eg. 2D grdid)
size = 64
space = GridSpaceSingle((size, size); periodic = true)

# number of agents
numagents = 64
numsteps = 256


#
# agent
#
# fields
@agent PingAgent{} GridAgent{2} begin
    wealth::Real
    contrib::Real
    test::ComplexF64
end

# step function
function agent_step!(agent, model)
    # println("My position is: ", agent.pos)
    # println("My id is: ", agent.id)
    randomwalk!(agent, model, 1)
    agent.test = agent.test + randn(ComplexF64)
    for nb in nearby_agents(agent, model, 2)
        if abs(nb.test) > abs(agent.test)
            agent.contrib += 1
        end 
    end
    # print(nearby_ids(agent,model,3))
end

# model
# implementing interactions
scheduler = Schedulers.randomly
model = ABM(
    PingAgent, 
    space;
    scheduler
    )


# simulation
# create agents
println("Agents: ", nagents(model))
for n in 1:numagents 
    agent = PingAgent(n, (1,1), 1.0, 0.0, 0.0)
    add_agent_single!(agent, model)
end

println("Agents: ", nagents(model))
function mean_contrib(model)
    function ret(model) 
        for ma in model.agents
            if ma.contrib > 1
                print(ma.contrib)
            end
        end
    end
    return [ret]
end

# run the model
rand_prop(agent) = agent.test
adata = [rand_prop, :contrib]
agent_data, model_data = run!(model, agent_step!, numsteps; adata)
println(agent_data[128:256, :])