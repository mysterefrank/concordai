from pydantic import BaseModel, Field
from typing import List

class ChatMessage(BaseModel):
    speaker: str
    message: str

class Conversation(BaseModel):
    topic: str
    messages: List[ChatMessage] = Field(default_factory=list)

    def add_message(self, message: ChatMessage):
        self.messages.append(message)

    def get_recent_messages(self, n: int = 5) -> List[ChatMessage]:
        return self.messages[-n:]
    
    def format_messages_for_openai(self, name: str, system_prompt: str):
        formatted_messages = [{"role": "system", "content": system_prompt}]
        for message in self.messages:
            if message.speaker == name:
                role = "system"
            else:
                role = "user"
            formatted_messages.append({
                "role": role,
                "content": f"{message.speaker}: {message.message}"
            })
        return formatted_messages
