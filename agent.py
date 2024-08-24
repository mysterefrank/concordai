from typing import List, Dict, Tuple, Any
import random
from openai import OpenAI
import os 
from conversation import Conversation, ChatMessage

class Agent:
    def __init__(self, name: str,  personality_prompt: str, model: Any = "meta-llama/llama-3.1-8b-instruct:free"):
        self.name = name
        self.personality_prompt = personality_prompt
        self.model = model
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY")
        )

    def calculate_bid(self, conversation_history: Conversation, topic: str) -> Tuple[float, float]:
        # Base implementation - can be overridden in subclasses
        calculate_bid_prompt = """
        
        """
        relevance = random.uniform(0, 1)
        confidence = random.uniform(0, 1)
        return relevance, confidence

    def generate_response(self, conversation_history: Conversation, topic: str, system_prompt: str) -> str:
        # Base implementation - should be overridden in subclasses
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=conversation_history.format_messages_for_openai(self.name, system_prompt + self.personality_prompt)
            )
        
        response = completion.choices[0].message.content

        # Remove the agent's name if it appears at the start of the response
        if response.lower().startswith(self.name.lower()):
            response = response[len(self.name):].lstrip(': ')

        return response

class Mediator(Agent):
    # Note: This is a different class because we'll later have a bunch of training logic for it.
    def __init__(self, personality_prompt: str, model: Any = "meta-llama/llama-3.1-8b-instruct:free"):
        super().__init__("Friendly Mediator", personality_prompt=personality_prompt, model=model)
