from pydantic import BaseModel, EmailStr


class CreateUserInputDTO(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str


class CreateUserOutputDTO(BaseModel):
    id: str
    name: str
    email: str
