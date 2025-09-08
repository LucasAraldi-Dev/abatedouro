from datetime import datetime
from typing import Optional, Annotated
from pydantic import BaseModel, Field, BeforeValidator, validator, EmailStr
from bson import ObjectId


def validate_object_id(v):
    if isinstance(v, ObjectId):
        return str(v)
    if isinstance(v, str):
        if ObjectId.is_valid(v):
            return v
        raise ValueError("Invalid ObjectId")
    raise ValueError("Invalid ObjectId")


PyObjectId = Annotated[str, BeforeValidator(validate_object_id)]


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Nome de usuário (único)")
    nome_completo: str = Field(..., min_length=2, max_length=100, description="Nome completo do usuário")
    email: EmailStr = Field(..., description="Email do usuário")


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, description="Senha do usuário")
    confirm_password: str = Field(..., min_length=6, description="Confirmação de senha")

    @validator("confirm_password")
    def passwords_match(cls, v, values):
        if "password" in values and v != values["password"]:
            raise ValueError("As senhas não conferem")
        return v


class UserInDB(UserBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    password_hash: str
    is_active: bool = False
    created_at: datetime

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class UserPublic(UserBase):
    is_active: bool
    created_at: datetime