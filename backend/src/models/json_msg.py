from pydantic import BaseModel


class JsonMsg(BaseModel):
    message: str


class JsonMsgSuccess(BaseModel):
    message: str
    success: bool
