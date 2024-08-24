import yaml
from string import Template
from chat_simulator import SimulationEnvironment
from agent import Agent, Mediator

def load_config():
    with open('config.yaml', 'r') as file:
        return yaml.safe_load(file)

config = load_config()

# Create agents
agents = []
for agent_config in config['agents']:
    agent = Agent(name=agent_config['name'], personality_prompt=agent_config['prompt'], model=config['model'])
    agents.append(agent)

# Create mediator
mediator = Mediator(personality_prompt=config['mediator']['prompt'], model=config['model'])

model = config['model']
# We have to use this template thing because the string is stored in a yaml. Means we can't use f strings.
system_prompt = Template(config['system_prompt']).safe_substitute(config['simulation'])
env = SimulationEnvironment(topic="Climate Change", agents=agents, mediator=mediator, system_prompt=system_prompt)

while not env.is_done():
    turn = env.step()
    print(f"{turn.speaker}: {turn.message}")

final_state = env.get_state()