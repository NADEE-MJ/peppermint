from pydantic import BaseModel


class Token(BaseModel):
    access_token: str


class TokenAndAdminResponse(Token):
    is_admin: bool


class TokenPayload(BaseModel):
    sub: str
