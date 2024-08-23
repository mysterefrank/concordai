from chat_simulator import SimulationEnvironment
from agent import Agent, Mediator

agent1 = Agent(name="Agent 1", model="gpt-3.5-turbo")
agent2 = Agent(name="Agent 2", model="gpt-3.5-turbo")
agent3 = Agent(name="Agent 3", model="gpt-3.5-turbo")
mediator = Mediator(model="gpt-3.5-turbo")

env = SimulationEnvironment(topic="Climate Change", agents=[agent1, agent2, agent3], mediator=mediator)

while not env.is_done():
    turn = env.step()
    print(f"{turn.speaker}: {turn.message}")

final_state = env.get_state()