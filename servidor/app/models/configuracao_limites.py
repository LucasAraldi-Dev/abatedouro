from pydantic import BaseModel, Field, field_validator
from typing import Optional, Any
from datetime import datetime
from bson import ObjectId

class ConfiguracaoLimitesBase(BaseModel):
    """Modelo base para configuração de limites e alertas"""
    # Limites de Performance
    rendimento_minimo: float = Field(default=80.0, ge=0, le=100, description="Rendimento mínimo esperado (%)")
    rendimento_ideal: float = Field(default=85.0, ge=0, le=100, description="Rendimento ideal esperado (%)")
    
    # Limites de Lucro
    lucro_minimo_por_ave: float = Field(default=5.0, ge=0, description="Lucro mínimo por ave (R$)")
    lucro_ideal_por_ave: float = Field(default=8.0, ge=0, description="Lucro ideal por ave (R$)")
    
    # Limites de Eficiência Operacional
    aves_por_hora_minimo: float = Field(default=80.0, ge=0, description="Aves por hora mínimo")
    aves_por_hora_ideal: float = Field(default=120.0, ge=0, description="Aves por hora ideal")
    
    # Limites de Qualidade
    peso_medio_minimo: float = Field(default=1.8, ge=0, description="Peso médio mínimo por ave (kg)")
    peso_medio_ideal: float = Field(default=2.2, ge=0, description="Peso médio ideal por ave (kg)")
    
    # Limites de Custos
    custo_operacional_maximo_por_ave: float = Field(default=3.0, ge=0, description="Custo operacional máximo por ave (R$)")
    custo_operacional_ideal_por_ave: float = Field(default=2.5, ge=0, description="Custo operacional ideal por ave (R$)")
    
    # Limites de Perdas
    percentual_perdas_maximo: float = Field(default=15.0, ge=0, le=100, description="Percentual máximo de perdas aceitável (%)")
    
    # Configurações de Alertas
    alertas_ativos: bool = Field(default=True, description="Se os alertas estão ativos")
    alerta_rendimento_baixo: bool = Field(default=True, description="Alerta para rendimento baixo")
    alerta_lucro_baixo: bool = Field(default=True, description="Alerta para lucro baixo")
    alerta_eficiencia_baixa: bool = Field(default=True, description="Alerta para eficiência baixa")
    alerta_qualidade_baixa: bool = Field(default=True, description="Alerta para qualidade baixa")
    alerta_custo_alto: bool = Field(default=True, description="Alerta para custo alto")

class ConfiguracaoLimitesCreate(ConfiguracaoLimitesBase):
    """Modelo para criação de configuração de limites"""
    pass

class ConfiguracaoLimitesUpdate(BaseModel):
    """Modelo para atualização de configuração de limites"""
    rendimento_minimo: Optional[float] = Field(None, ge=0, le=100)
    rendimento_ideal: Optional[float] = Field(None, ge=0, le=100)
    lucro_minimo_por_ave: Optional[float] = Field(None, ge=0)
    lucro_ideal_por_ave: Optional[float] = Field(None, ge=0)
    aves_por_hora_minimo: Optional[float] = Field(None, ge=0)
    aves_por_hora_ideal: Optional[float] = Field(None, ge=0)
    peso_medio_minimo: Optional[float] = Field(None, ge=0)
    peso_medio_ideal: Optional[float] = Field(None, ge=0)
    custo_operacional_maximo_por_ave: Optional[float] = Field(None, ge=0)
    custo_operacional_ideal_por_ave: Optional[float] = Field(None, ge=0)
    percentual_perdas_maximo: Optional[float] = Field(None, ge=0, le=100)
    alertas_ativos: Optional[bool] = None
    alerta_rendimento_baixo: Optional[bool] = None
    alerta_lucro_baixo: Optional[bool] = None
    alerta_eficiencia_baixa: Optional[bool] = None
    alerta_qualidade_baixa: Optional[bool] = None
    alerta_custo_alto: Optional[bool] = None

class ConfiguracaoLimites(ConfiguracaoLimitesBase):
    """Modelo completo de configuração de limites"""
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