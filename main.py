from chat_simulator import SimulationEnvironment
from agent import Agent, Mediator

agent1 = Agent(name="Dr. Samantha Chen", personality_prompt="Climate Scientist, Age: 42 Background: A renowned climatologist with a Ph.D. from MIT, Samantha has dedicated her career to studying the effects of climate change. She's published numerous papers on the subject and has participated in several international climate conferences. Samantha is passionate about educating the public on the scientific consensus regarding global warming.")
agent2 = Agent(name="Bob Miller", personality_prompt="Small Town Business Owner Age: 58 Background: Bob runs a family-owned manufacturing plant in a rust belt town. The plant has been in his family for three generations. He's skeptical of climate change theories, viewing them as potential threats to his business and community. Bob is concerned about job losses and economic impact that might result from strict environmental regulations.")
agent3 = Agent(name="Zoe Martinez ", personality_prompt="Environmental Activist Age: 25 Background: A recent college graduate with a degree in Environmental Studies, Zoe is a grassroots organizer for a climate action group. She's idealistic and impatient for change, often clashing with those she sees as moving too slowly on environmental issues. Zoe comes from a coastal community already experiencing the effects of rising sea levels.")
mediator = Mediator("Skilled mediator")

env = SimulationEnvironment(topic="Climate Change", agents=[agent1, agent2, agent3], mediator=mediator)

while not env.is_done():
    turn = env.step()
    print(f"{turn.speaker}: {turn.message}")

final_state = env.get_state()