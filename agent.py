from typing import List, Dict, Tuple, Any
import random
from openai import OpenAI
import os 
from conversation import Conversation, ChatMessage

class Agent:
    def __init__(self, name: str, model: Any):
        self.name = name
        self.personality_prompt = None
        self.model = model
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY")
        )

    def calculate_bid(self, conversation_history: Conversation, topic: str) -> Tuple[float, float]:
        # Base implementation - can be overridden in subclasses
        relevance = random.uniform(0, 1)
        confidence = random.uniform(0, 1)
        return relevance, confidence

    def generate_response(self, conversation_history: Conversation, topic: str) -> str:
        # Base implementation - should be overridden in subclasses
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=conversation_history.format_messages_for_openai(self.name)
            )
        print(completion.choices[0].message.content)
        import pdb; pdb.set_trace()

class Mediator(Agent):
    def __init__(self, model: Any):
        super().__init__("Friendly Mediator", model)

    def calculate_bid(self, conversation_history: Conversation, topic: str) -> Tuple[float, float]:
        # Mediator-specific bidding logic
        # This could be based on detecting need for intervention, conversation flow, etc.
        relevance = random.uniform(0, 1)  # Mediator might have a higher base relevance
        confidence = random.uniform(0, 1)  # Mediator might be generally more confident
        return relevance, confidence

    def generate_response(self, conversation_history: Conversation, topic: str) -> str:
        # Implement mediator-specific response generation logic
        # This could focus on guiding the conversation, finding common ground, etc.
        pass