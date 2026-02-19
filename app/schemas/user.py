from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


# 🔹 Schema para criação de usuário
class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=72)


# 🔹 Schema para resposta ao cliente (não retorna senha)
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    plan: str
    is_active: bool
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True
