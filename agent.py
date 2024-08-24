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
        calculate_bid_prompt = f"""
        You are {self.name}.

        Given the conversation history and the current topic, evaluate how relevant and confident you feel about contributing to the conversation next.

        Topic: {topic}
        Recent conversation:
        {conversation_history.get_recent_messages(5)}

        Please respond with two numbers between 0 and 1, separated by a comma:
        - The first number represents your relevance score (how relevant you feel your input would be)
        - The second number represents your confidence score (how confident you are in providing valuable input)

        For example: 0.8, 0.7

        Relevance, Confidence:
        """

        completion = self.client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[{"role": "user", "content": calculate_bid_prompt}]
        )

        response = completion.choices[0].message.content.strip()
        print(response)
        try:
            relevance, confidence = map(float, response.split(','))
            return min(max(relevance, 0), 1), min(max(confidence, 0), 1)
        except ValueError:
            # If parsing fails, return random values as a fallback
            return random.uniform(0, 1), random.uniform(0, 1)

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
