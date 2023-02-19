from pydantic import BaseModel


class JsonMsg(BaseModel):
    message: str
