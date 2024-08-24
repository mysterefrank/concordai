from typing import List, Dict, Any
import random
from conversation import Conversation, ChatMessage

class SimulationEnvironment:
    def __init__(self, topic: str, agents: List[Any], mediator: Any, system_prompt: str = ""):
        self.topic = topic
        self.agents = agents
        self.mediator = mediator
        self.conversation_history = Conversation(topic=topic)
        self.current_speaker = None
        self.system_prompt = system_prompt

    def _get_bids(self) -> List[Dict[str, Any]]:
        bids = []
        for agent in self.agents:
            relevance, confidence = agent.calculate_bid(self.conversation_history, self.topic)
            bids.append({
                "agent": agent,
                "relevance": relevance,
                "confidence": confidence,
                "score": relevance * confidence
            })
        
        # Mediator's bid
        mediator_relevance, mediator_confidence = self.mediator.calculate_bid(self.conversation_history, self.topic)
        bids.append({
            "agent": self.mediator,
            "relevance": mediator_relevance,
            "confidence": mediator_confidence,
            "score": mediator_relevance * mediator_confidence
        })
        
        return bids

    def _select_next_speaker(self, bids: List[Dict[str, Any]]) -> Any:
        # Sort bids by score in descending order
        sorted_bids = sorted(bids, key=lambda x: x['score'], reverse=True)
        
        # Select the top bid, with some randomness to prevent always choosing the highest score
        if random.random() < 0.8:  # 80% chance of choosing the top bid
            return sorted_bids[0]['agent']
        else:
            # 20% chance of choosing randomly from top 3 bids (if available)
            return random.choice(sorted_bids[:min(3, len(sorted_bids))])['agent']

    def step(self) -> Dict[str, str]:
        bids = self._get_bids()
        self.current_speaker = self._select_next_speaker(bids)
        
        if self.current_speaker == self.mediator:
            message = self.mediator.generate_response(self.conversation_history, self.topic, self.system_prompt)
        else:
            message = self.current_speaker.generate_response(self.conversation_history, self.topic, self.system_prompt)

        turn = ChatMessage(message=str(message), speaker=self.current_speaker.name)
        self.conversation_history.add_message(turn)
        return turn

    def get_state(self) -> Dict[str, Any]:
        return {
            "topic": self.topic,
            "conversation_history": self.conversation_history,
            "current_speaker": self.current_speaker
        }

    def measure_consensus(self) -> float:
        # Implement logic to calculate consensus level
        pass

    def save_state(self, filename: str):
        # Implement state saving logic
        pass

    def load_state(self, filename: str):
        # Implement state loading logic
        pass

    def update_agent_states(self):
        for agent in self.agents:
            agent.update_state(self.conversation_history, self.topic)
            
    def is_done(self) -> bool:
        # Implement your termination condition here
        # For example, end after a certain number of turns or when consensus is reached
        return len(self.conversation_history.messages) >= 50  # Example condition