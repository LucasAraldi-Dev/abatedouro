from datetime import datetime
from typing import Optional, Annotated
from pydantic import BaseModel, Field, BeforeValidator
from bson import ObjectId


# Validador para ObjectId
def validate_object_id(v):
    if isinstance(v, str):
        return ObjectId(v)
    return v


PyObjectId = Annotated[ObjectId, BeforeValidator(validate_object_id)]


class ProdutoLogBase(BaseModel):
    produto_id: PyObjectId = Field(..., description="ID do produto")
    tipo_alteracao: str = Field(..., description="Tipo de alteração (edicao, atualizacao_preco)")
    campo_alterado: str = Field(..., description="Campo que foi alterado")
    valor_anterior: str = Field(..., description="Valor anterior")
    valor_novo: str = Field(..., description="Novo valor")
    data_alteracao: datetime = Field(default_factory=datetime.now, description="Data da alteração")
    usuario: Optional[str] = Field(default="Sistema", description="Usuário que fez a alteração")
    observacoes: Optional[str] = Field(None, description="Observações sobre a alteração")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda v: v.isoformat()
        }


class ProdutoLogCreate(ProdutoLogBase):
    pass


class ProdutoLog(ProdutoLogBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda v: v.isoformat()
        }


class ProdutoLogResponse(BaseModel):
    id: str
    produto_id: str
    tipo_alteracao: str
    campo_alterado: str
    valor_anterior: str
    valor_novo: str
    data_alteracao: datetime
    usuario: str
    observacoes: Optional[str] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }