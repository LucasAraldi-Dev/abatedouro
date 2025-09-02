from datetime import datetime
from typing import Optional, List, Dict, Any, Annotated
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


class ProdutoAbate(BaseModel):
    """Modelo para produtos processados no abate"""
    produto_id: Optional[str] = None
    nome: str = Field(..., description="Nome do produto")
    tipo: str = Field(..., description="Tipo do produto")
    peso_kg: float = Field(..., gt=0, description="Peso em kg")
    preco_kg: float = Field(..., gt=0, description="Preço por kg")
    valor_total: float = Field(..., gt=0, description="Valor total do produto")
    percentual: Optional[float] = Field(None, description="Percentual do produto")


class DespesasFixas(BaseModel):
    """Modelo para despesas fixas do abate"""
    funcionarios: float = Field(default=0, ge=0)
    agua: float = Field(default=0, ge=0)
    energia: float = Field(default=0, ge=0)
    embalagem: float = Field(default=0, ge=0)
    refeicao: float = Field(default=0, ge=0)
    materiais_limpeza: float = Field(default=0, ge=0)
    gelo: float = Field(default=0, ge=0)
    horas_extras: float = Field(default=0, ge=0)
    amonia: float = Field(default=0, ge=0)
    epi: float = Field(default=0, ge=0)
    manutencao: float = Field(default=0, ge=0)
    lenha_caldeira: float = Field(default=0, ge=0)
    diaristas: float = Field(default=0, ge=0)
    depreciacao: float = Field(default=0, ge=0)
    recisao: float = Field(default=0, ge=0)
    ferias: float = Field(default=0, ge=0)
    inss: float = Field(default=0, ge=0)
    frango_morto_plataforma: float = Field(default=0, ge=0)
    escaldagem_eviceracao: float = Field(default=0, ge=0)
    pe_graxaria: float = Field(default=0, ge=0)
    descarte: float = Field(default=0, ge=0)


class HorariosAbate(BaseModel):
    """Modelo para horários do abate"""
    hora_inicio: str = Field(..., description="Hora de início")
    hora_termino: str = Field(..., description="Hora de término")
    intervalo_minutos: int = Field(default=0, ge=0, description="Intervalo em minutos")
    horas_trabalhadas: float = Field(default=0, ge=0, description="Horas trabalhadas")
    horas_reais: float = Field(default=0, ge=0, description="Horas reais")


class AbateCompletoBase(BaseModel):
    """Modelo base completo para abate"""
    # Dados básicos
    data_abate: datetime = Field(..., description="Data do abate")
    quantidade_aves: int = Field(..., gt=0, description="Quantidade de aves abatidas")
    valor_kg_vivo: float = Field(..., gt=0, description="Valor por kg vivo")
    peso_total_kg: float = Field(..., gt=0, description="Peso total em kg")
    peso_medio_ave: float = Field(default=0, ge=0, description="Peso médio por ave")
    valor_total: float = Field(default=0, ge=0, description="Valor total")
    
    # Dados gerais
    unidade: str = Field(..., min_length=1, max_length=100, description="Unidade/Local do abate")
    tipo_ave: str = Field(default="frango", description="Tipo de ave")
    observacoes: Optional[str] = Field(None, max_length=500, description="Observações adicionais")
    
    # Horários
    horarios: HorariosAbate = Field(..., description="Horários do abate")
    
    # Produtos processados
    produtos: List[ProdutoAbate] = Field(default=[], description="Produtos processados")
    
    # Despesas fixas
    despesas_fixas: DespesasFixas = Field(default_factory=DespesasFixas, description="Despesas fixas")
    
    # Dados financeiros adicionais
    peso_inteiro_abatido: float = Field(default=0, ge=0, description="Peso inteiro abatido")
    preco_venda_kg: float = Field(default=0, ge=0, description="Preço de venda por kg")
    
    # Indicadores de Performance Calculados
    # Métricas principais
    receita_bruta: Optional[float] = Field(default=None, ge=0, description="Receita bruta total")
    custos_totais: Optional[float] = Field(default=None, ge=0, description="Custos totais")
    lucro_liquido: Optional[float] = Field(default=None, description="Lucro líquido")
    rendimento_final: Optional[float] = Field(default=None, ge=0, le=100, description="Rendimento final em %")
    
    # Indicadores por unidade
    media_valor_kg: Optional[float] = Field(default=None, ge=0, description="Média valor por kg processado")
    custo_kg: Optional[float] = Field(default=None, ge=0, description="Custo por kg")
    custo_ave: Optional[float] = Field(default=None, ge=0, description="Custo por ave")
    custo_abate_kg: Optional[float] = Field(default=None, ge=0, description="Custo de abate por kg")
    custo_frango: Optional[float] = Field(default=None, ge=0, description="Custo por frango")
    lucro_kg: Optional[float] = Field(default=None, description="Lucro por kg")
    lucro_frango: Optional[float] = Field(default=None, description="Lucro por frango")
    lucro_total: Optional[float] = Field(default=None, description="Lucro total do dia")
    
    # Percentuais dos indicadores
    percentual_media_valor_kg: Optional[float] = Field(default=None, ge=0, le=100, description="% Média valor/kg")
    percentual_custo_kg: Optional[float] = Field(default=None, ge=0, le=100, description="% Custo/kg")
    percentual_custo_ave: Optional[float] = Field(default=None, ge=0, le=100, description="% Custo por ave")
    percentual_custo_abate_kg: Optional[float] = Field(default=None, ge=0, le=100, description="% Custo abate/kg")
    percentual_custo_frango: Optional[float] = Field(default=None, ge=0, le=100, description="% Custo por frango")
    percentual_lucro_kg: Optional[float] = Field(default=None, description="% Lucro/kg")
    percentual_lucro_frango: Optional[float] = Field(default=None, description="% Lucro por frango")
    percentual_lucro_total: Optional[float] = Field(default=None, description="% Lucro total")
    percentual_rendimento: Optional[float] = Field(default=None, ge=0, le=100, description="% Rendimento")

    class Config:
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "data_abate": "2024-01-15T08:00:00",
                "quantidade_aves": 100,
                "valor_kg_vivo": 5.50,
                "peso_total_kg": 180.5,
                "peso_medio_ave": 1.805,
                "valor_total": 992.75,
                "unidade": "Unidade Principal",
                "tipo_ave": "frango",
                "observacoes": "Lote de qualidade superior",
                "horarios": {
                    "hora_inicio": "06:00",
                    "hora_termino": "14:00",
                    "intervalo_minutos": 60,
                    "horas_trabalhadas": 7.0,
                    "horas_reais": 8.0
                },
                "produtos": [
                    {
                        "nome": "Frango Inteiro",
                        "tipo": "Carcaça",
                        "peso_kg": 150.0,
                        "preco_kg": 12.50,
                        "valor_total": 1875.0,
                        "percentual": 83.1
                    }
                ],
                "despesas_fixas": {
                    "funcionarios": 200.0,
                    "agua": 50.0,
                    "energia": 80.0
                },
                "peso_inteiro_abatido": 150.0,
                "preco_venda_kg": 12.50
            }
        }


class AbateCompletoCreate(AbateCompletoBase):
    """Modelo para criação de abate completo"""
    pass


class AbateCompletoUpdate(BaseModel):
    """Modelo para atualização de abate completo"""
    data_abate: Optional[datetime] = None
    quantidade_aves: Optional[int] = Field(None, gt=0)
    valor_kg_vivo: Optional[float] = Field(None, gt=0)
    peso_total_kg: Optional[float] = Field(None, gt=0)
    peso_medio_ave: Optional[float] = Field(None, ge=0)
    valor_total: Optional[float] = Field(None, ge=0)
    unidade: Optional[str] = Field(None, min_length=1, max_length=100)
    tipo_ave: Optional[str] = None
    observacoes: Optional[str] = Field(None, max_length=500)
    horarios: Optional[HorariosAbate] = None
    produtos: Optional[List[ProdutoAbate]] = None
    despesas_fixas: Optional[DespesasFixas] = None
    peso_inteiro_abatido: Optional[float] = Field(None, ge=0)
    preco_venda_kg: Optional[float] = Field(None, ge=0)
    
    # Indicadores de Performance Calculados (opcionais para update)
    receita_bruta: Optional[float] = Field(None, ge=0)
    custos_totais: Optional[float] = Field(None, ge=0)
    lucro_liquido: Optional[float] = None
    rendimento_final: Optional[float] = Field(None, ge=0, le=100)
    media_valor_kg: Optional[float] = Field(None, ge=0)
    custo_kg: Optional[float] = Field(None, ge=0)
    custo_ave: Optional[float] = Field(None, ge=0)
    custo_abate_kg: Optional[float] = Field(None, ge=0)
    custo_frango: Optional[float] = Field(None, ge=0)
    lucro_kg: Optional[float] = None
    lucro_frango: Optional[float] = None
    lucro_total: Optional[float] = None
    percentual_media_valor_kg: Optional[float] = Field(None, ge=0, le=100)
    percentual_custo_kg: Optional[float] = Field(None, ge=0, le=100)
    percentual_custo_ave: Optional[float] = Field(None, ge=0, le=100)
    percentual_custo_abate_kg: Optional[float] = Field(None, ge=0, le=100)
    percentual_custo_frango: Optional[float] = Field(None, ge=0, le=100)
    percentual_lucro_kg: Optional[float] = None
    percentual_lucro_frango: Optional[float] = None
    percentual_lucro_total: Optional[float] = None
    percentual_rendimento: Optional[float] = Field(None, ge=0, le=100)


class AbateCompletoInDB(AbateCompletoBase):
    """Modelo de abate completo no banco de dados"""
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class AbateCompleto(AbateCompletoInDB):
    """Modelo final de abate completo"""
    pass