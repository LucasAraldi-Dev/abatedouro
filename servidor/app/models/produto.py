from datetime import datetime
from typing import Optional, Annotated
from pydantic import BaseModel, Field, BeforeValidator, validator
from bson import ObjectId
from decimal import Decimal, ROUND_HALF_UP


def validate_object_id(v):
    if isinstance(v, ObjectId):
        return str(v)
    if isinstance(v, str):
        if ObjectId.is_valid(v):
            return v
        raise ValueError("Invalid ObjectId")
    raise ValueError("Invalid ObjectId")


PyObjectId = Annotated[str, BeforeValidator(validate_object_id)]


class ProdutoBase(BaseModel):
    nome: str = Field(..., min_length=1, max_length=100, description="Nome do produto/corte")
    tipo: str = Field(..., min_length=1, max_length=50, description="Tipo do produto (peito, coxa, asa, etc.)")
    preco_kg: float = Field(..., gt=0, description="Preço por kg")
    unidade_origem: str = Field(..., min_length=1, max_length=100, description="Unidade de origem")
    
    @validator('preco_kg')
    def validate_preco_kg(cls, v):
        # Arredonda para 2 casas decimais
        return float(Decimal(str(v)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))

    class Config:
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "nome": "Peito de Frango",
                "tipo": "peito",
                "preco_kg": 12.50,
                "unidade_origem": "Unidade Principal"
            }
        }


class ProdutoCreate(ProdutoBase):
    pass


class ProdutoUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=1, max_length=100)
    tipo: Optional[str] = Field(None, min_length=1, max_length=50)
    preco_kg: Optional[float] = Field(None, gt=0)
    unidade_origem: Optional[str] = Field(None, min_length=1, max_length=100)
    
    @validator('preco_kg')
    def validate_preco_kg(cls, v):
        if v is not None:
            # Arredonda para 2 casas decimais
            return float(Decimal(str(v)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
        return v


class ProdutoInDB(ProdutoBase):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class Produto(ProdutoInDB):
    pass