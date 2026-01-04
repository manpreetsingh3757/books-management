from pydantic import BaseModel, Field, EmailStr

class LoginUser(BaseModel):
    email: EmailStr
    password: str

class LoginToken(BaseModel):
    access_token: str
    token_type: str = Field(default="bearer")
