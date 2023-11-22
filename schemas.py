from pydantic import BaseModel


class Message(BaseModel):
    message: str
    message_hash: str
    message_salt: str
