import yaml
from string import Template
from chat_simulator import SimulationEnvironment
from agent import Agent, Mediator

def load_config(filename='config.yaml'):
    with open(filename, 'r') as file:
        return yaml.safe_load(file)

def create_agents(agent_configs, model):
    return [Agent(name=cfg['name'], personality_prompt=cfg['prompt'], model=model) for cfg in agent_configs]

def main():
    config = load_config()
    model = config['model']
    agents = create_agents(config['agents'], model)
    mediator = Mediator(personality_prompt=config['mediator']['prompt'], model=model)

    system_prompt = Template(config['system_prompt']).safe_substitute(config['simulation'])
    env = SimulationEnvironment(
        topic=config['simulation']['topic'],
        agents=agents,
        mediator=mediator,
        system_prompt=system_prompt
    )

    while not env.is_done():
        turn = env.step()
        print(f"{turn.speaker}: {turn.message}")

    # Don't have a solid idea yet when the conversation should end but for now it's after 50 turns.
    final_state = env.get_state()
    # This is when we'd evaluate consensus and from that get a reward signal for the mediator.
if __name__ == "__main__":
    main()