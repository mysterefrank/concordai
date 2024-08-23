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
    
    def make_egocentric(self, name):
        # TODO: Make sure this is a copy of the object
        for message in self.messages:
            if message.speaker == name:
                message.speaker = "system"
            else:
                message.speaker = "user"
        return self