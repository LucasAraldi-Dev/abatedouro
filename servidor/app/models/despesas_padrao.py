from pydantic import BaseModel, Field, field_validator
from typing import Optional, Any
from datetime import datetime
from bson import ObjectId

class DespesasPadraoBase(BaseModel):
    """Modelo base para despesas padrão"""
    funcionarios: float = Field(default=0.0, ge=0, description="Valor padrão para funcionários")
    agua: float = Field(default=0.0, ge=0, description="Valor padrão para água")
    energia: float = Field(default=0.0, ge=0, description="Valor padrão para energia")
    embalagem: float = Field(default=0.0, ge=0, description="Valor padrão para embalagem")
    refeicao: float = Field(default=0.0, ge=0, description="Valor padrão para refeição")
    materiais_limpeza: float = Field(default=0.0, ge=0, description="Valor padrão para materiais de limpeza")
    gelo: float = Field(default=0.0, ge=0, description="Valor padrão para gelo")
    horas_extras: float = Field(default=0.0, ge=0, description="Valor padrão para horas extras")
    amonia: float = Field(default=0.0, ge=0, description="Valor padrão para amônia")
    epi: float = Field(default=0.0, ge=0, description="Valor padrão para EPI")
    manutencao: float = Field(default=0.0, ge=0, description="Valor padrão para manutenção")
    lenha_caldeira: float = Field(default=0.0, ge=0, description="Valor padrão para lenha/caldeira")
    diaristas: float = Field(default=0.0, ge=0, description="Valor padrão para diaristas")
    depreciacao: float = Field(default=0.0, ge=0, description="Valor padrão para depreciação")
    recisao: float = Field(default=0.0, ge=0, description="Valor padrão para rescisão")
    ferias: float = Field(default=0.0, ge=0, description="Valor padrão para férias")
    inss: float = Field(default=0.0, ge=0, description="Valor padrão para INSS")
    frango_morto_plataforma: float = Field(default=0.0, ge=0, description="Valor padrão para frango morto plataforma")
    escaldagem_eviceracao: float = Field(default=0.0, ge=0, description="Valor padrão para escaldagem/evisceração")
    pe_graxaria: float = Field(default=0.0, ge=0, description="Valor padrão para pé/graxaria")
    descarte: float = Field(default=0.0, ge=0, description="Valor padrão para descarte")

class DespesasPadraoCreate(DespesasPadraoBase):
    """Modelo para criação de despesas padrão"""
    pass

class DespesasPadraoUpdate(BaseModel):
    """Modelo para atualização de despesas padrão"""
    funcionarios: Optional[float] = Field(None, ge=0)
    agua: Optional[float] = Field(None, ge=0)
    energia: Optional[float] = Field(None, ge=0)
    embalagem: Optional[float] = Field(None, ge=0)
    refeicao: Optional[float] = Field(None, ge=0)
    materiais_limpeza: Optional[float] = Field(None, ge=0)
    gelo: Optional[float] = Field(None, ge=0)
    horas_extras: Optional[float] = Field(None, ge=0)
    amonia: Optional[float] = Field(None, ge=0)
    epi: Optional[float] = Field(None, ge=0)
    manutencao: Optional[float] = Field(None, ge=0)
    lenha_caldeira: Optional[float] = Field(None, ge=0)
    diaristas: Optional[float] = Field(None, ge=0)
    depreciacao: Optional[float] = Field(None, ge=0)
    recisao: Optional[float] = Field(None, ge=0)
    ferias: Optional[float] = Field(None, ge=0)
    inss: Optional[float] = Field(None, ge=0)
    frango_morto_plataforma: Optional[float] = Field(None, ge=0)
    escaldagem_eviceracao: Optional[float] = Field(None, ge=0)
    pe_graxaria: Optional[float] = Field(None, ge=0)
    descarte: Optional[float] = Field(None, ge=0)

class DespesasPadrao(DespesasPadraoBase):
    """Modelo completo de despesas padrão"""
    id: Optional[str] = Field(None, alias="_id")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    @field_validator('id', mode='before')
    @classmethod
    def validate_id(cls, v: Any) -> Optional[str]:
        if isinstance(v, ObjectId):
            return str(v)
        return v
    
    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda v: v.isoformat()
        }