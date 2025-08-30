from datetime import datetime
from typing import Optional, Annotated
from pydantic import BaseModel, Field, BeforeValidator
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


class LoteAbateBase(BaseModel):
    data_abate: datetime = Field(..., description="Data do abate")
    quantidade_aves: int = Field(..., gt=0, description="Quantidade de aves abatidas")
    peso_total_kg: float = Field(..., gt=0, description="Peso total em kg")
    unidade: str = Field(..., min_length=1, max_length=100, description="Unidade/Local do abate")
    tipo_ave: str = Field(default="frango", description="Tipo de ave (frango, galinha, etc.)")
    observacoes: Optional[str] = Field(None, max_length=500, description="Observações adicionais")

    class Config:
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "data_abate": "2024-01-15T08:00:00",
                "quantidade_aves": 100,
                "peso_total_kg": 180.5,
                "unidade": "Unidade Principal",
                "tipo_ave": "frango",
                "observacoes": "Lote de qualidade superior"
            }
        }


class LoteAbateCreate(LoteAbateBase):
    pass


class LoteAbateUpdate(BaseModel):
    data_abate: Optional[datetime] = None
    quantidade_aves: Optional[int] = Field(None, gt=0)
    peso_total_kg: Optional[float] = Field(None, gt=0)
    unidade: Optional[str] = Field(None, min_length=1, max_length=100)
    tipo_ave: Optional[str] = None
    observacoes: Optional[str] = Field(None, max_length=500)


class LoteAbateInDB(LoteAbateBase):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class LoteAbate(LoteAbateInDB):
    pass