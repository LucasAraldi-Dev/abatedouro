from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from motor.motor_asyncio import AsyncIOMotorDatabase

from ....core.database import get_db
from ....models.abate_completo import (
    AbateCompleto,
    AbateCompletoCreate,
    AbateCompletoUpdate
)
from ....crud.abate_completo import get_abate_completo_crud

router = APIRouter()


@router.post("/", response_model=dict, status_code=201)
async def create_abate_completo(
    abate_data: AbateCompletoCreate,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Criar um novo abate completo"""
    if db is None:
        raise HTTPException(status_code=500, detail="Erro de conexão com o banco de dados")
    
    crud = get_abate_completo_crud(db)
    try:
        abate = await crud.create(abate_data)
        return {
            "id": str(abate.id),
            "data_abate": abate.data_abate,
            "quantidade_aves": abate.quantidade_aves,
            "valor_kg_vivo": abate.valor_kg_vivo,
            "peso_total_kg": abate.peso_total_kg,
            "peso_medio_ave": abate.peso_medio_ave,
            "valor_total": abate.valor_total,
            "unidade": abate.unidade,
            "tipo_ave": abate.tipo_ave,
            "observacoes": abate.observacoes,
            "horarios": abate.horarios.model_dump(),
            "produtos": [produto.model_dump() for produto in abate.produtos],
            "despesas_fixas": abate.despesas_fixas.model_dump(),
            "peso_inteiro_abatido": abate.peso_inteiro_abatido,
            "preco_venda_kg": abate.preco_venda_kg,
            "created_at": abate.created_at,
            "updated_at": abate.updated_at
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar abate: {str(e)}")


@router.get("/", response_model=List[dict])
async def get_abates_completos(
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    unidade: Optional[str] = Query(None, description="Filtrar por unidade"),
    tipo_ave: Optional[str] = Query(None, description="Filtrar por tipo de ave"),
    data_inicio: Optional[str] = Query(None, description="Data de início (YYYY-MM-DD)"),
    data_fim: Optional[str] = Query(None, description="Data de fim (YYYY-MM-DD)"),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Listar abates completos com filtros"""
    if db is None:
        raise HTTPException(status_code=500, detail="Erro de conexão com o banco de dados")
    
    crud = get_abate_completo_crud(db)
    try:
        # Converter strings de data para datetime
        dt_inicio = None
        dt_fim = None
        
        if data_inicio:
            try:
                dt_inicio = datetime.fromisoformat(data_inicio)
            except ValueError:
                raise HTTPException(status_code=400, detail="Formato de data_inicio inválido. Use YYYY-MM-DD")
        
        if data_fim:
            try:
                dt_fim = datetime.fromisoformat(data_fim)
                # Incluir o dia inteiro
                dt_fim = dt_fim.replace(hour=23, minute=59, second=59, microsecond=999999)
            except ValueError:
                raise HTTPException(status_code=400, detail="Formato de data_fim inválido. Use YYYY-MM-DD")
        
        abates = await crud.get_many(
            skip=skip,
            limit=limit,
            unidade=unidade,
            tipo_ave=tipo_ave,
            data_inicio=dt_inicio,
            data_fim=dt_fim
        )
        
        return [
            {
                "id": str(abate.id),
                "data_abate": abate.data_abate,
                "quantidade_aves": abate.quantidade_aves,
                "valor_kg_vivo": abate.valor_kg_vivo,
                "peso_total_kg": abate.peso_total_kg,
                "peso_medio_ave": abate.peso_medio_ave,
                "valor_total": abate.valor_total,
                "unidade": abate.unidade,
                "tipo_ave": abate.tipo_ave,
                "observacoes": abate.observacoes,
                "horarios": abate.horarios.model_dump(),
                "produtos": [produto.model_dump() for produto in abate.produtos],
                "despesas_fixas": abate.despesas_fixas.model_dump(),
                "peso_inteiro_abatido": abate.peso_inteiro_abatido,
                "preco_venda_kg": abate.preco_venda_kg,
                "created_at": abate.created_at,
                "updated_at": abate.updated_at
            }
            for abate in abates
        ]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar abates: {str(e)}")


@router.get("/count", response_model=dict)
async def count_abates_completos(
    unidade: Optional[str] = Query(None, description="Filtrar por unidade"),
    tipo_ave: Optional[str] = Query(None, description="Filtrar por tipo de ave"),
    data_inicio: Optional[str] = Query(None, description="Data de início (YYYY-MM-DD)"),
    data_fim: Optional[str] = Query(None, description="Data de fim (YYYY-MM-DD)"),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Contar total de abates completos"""
    if db is None:
        raise HTTPException(status_code=500, detail="Erro de conexão com o banco de dados")
    
    crud = get_abate_completo_crud(db)
    try:
        # Converter strings de data para datetime
        dt_inicio = None
        dt_fim = None
        
        if data_inicio:
            try:
                dt_inicio = datetime.fromisoformat(data_inicio)
            except ValueError:
                raise HTTPException(status_code=400, detail="Formato de data_inicio inválido. Use YYYY-MM-DD")
        
        if data_fim:
            try:
                dt_fim = datetime.fromisoformat(data_fim)
                dt_fim = dt_fim.replace(hour=23, minute=59, second=59, microsecond=999999)
            except ValueError:
                raise HTTPException(status_code=400, detail="Formato de data_fim inválido. Use YYYY-MM-DD")
        
        total = await crud.count(
            unidade=unidade,
            tipo_ave=tipo_ave,
            data_inicio=dt_inicio,
            data_fim=dt_fim
        )
        return {"total": total}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao contar abates: {str(e)}")


@router.get("/periodo", response_model=List[dict])
async def get_abates_por_periodo(
    data_inicio: str = Query(..., description="Data de início (YYYY-MM-DD)"),
    data_fim: str = Query(..., description="Data de fim (YYYY-MM-DD)"),
    unidade: Optional[str] = Query(None, description="Filtrar por unidade"),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Buscar abates completos por período"""
    if db is None:
        raise HTTPException(status_code=500, detail="Erro de conexão com o banco de dados")
    
    crud = get_abate_completo_crud(db)
    try:
        # Converter strings de data para datetime
        try:
            dt_inicio = datetime.fromisoformat(data_inicio)
            dt_fim = datetime.fromisoformat(data_fim)
            dt_fim = dt_fim.replace(hour=23, minute=59, second=59, microsecond=999999)
        except ValueError:
            raise HTTPException(status_code=400, detail="Formato de data inválido. Use YYYY-MM-DD")
        
        abates = await crud.get_by_periodo(
            data_inicio=dt_inicio,
            data_fim=dt_fim,
            unidade=unidade
        )
        
        return [
            {
                "id": str(abate.id),
                "data_abate": abate.data_abate,
                "quantidade_aves": abate.quantidade_aves,
                "valor_kg_vivo": abate.valor_kg_vivo,
                "peso_total_kg": abate.peso_total_kg,
                "peso_medio_ave": abate.peso_medio_ave,
                "valor_total": abate.valor_total,
                "unidade": abate.unidade,
                "tipo_ave": abate.tipo_ave,
                "observacoes": abate.observacoes,
                "horarios": abate.horarios.model_dump(),
                "produtos": [produto.model_dump() for produto in abate.produtos],
                "despesas_fixas": abate.despesas_fixas.model_dump(),
                "peso_inteiro_abatido": abate.peso_inteiro_abatido,
                "preco_venda_kg": abate.preco_venda_kg,
                "created_at": abate.created_at,
                "updated_at": abate.updated_at
            }
            for abate in abates
        ]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar abates por período: {str(e)}")


@router.get("/{abate_id}", response_model=dict)
async def get_abate_completo(
    abate_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Buscar abate completo por ID"""
    if db is None:
        raise HTTPException(status_code=500, detail="Erro de conexão com o banco de dados")
    
    crud = get_abate_completo_crud(db)
    try:
        abate = await crud.get(abate_id)
        if not abate:
            raise HTTPException(status_code=404, detail="Abate não encontrado")
        
        return {
            "id": str(abate.id),
            "data_abate": abate.data_abate,
            "quantidade_aves": abate.quantidade_aves,
            "valor_kg_vivo": abate.valor_kg_vivo,
            "peso_total_kg": abate.peso_total_kg,
            "peso_medio_ave": abate.peso_medio_ave,
            "valor_total": abate.valor_total,
            "unidade": abate.unidade,
            "tipo_ave": abate.tipo_ave,
            "observacoes": abate.observacoes,
            "horarios": abate.horarios.model_dump(),
            "produtos": [produto.model_dump() for produto in abate.produtos],
            "despesas_fixas": abate.despesas_fixas.model_dump(),
            "peso_inteiro_abatido": abate.peso_inteiro_abatido,
            "preco_venda_kg": abate.preco_venda_kg,
            "created_at": abate.created_at,
            "updated_at": abate.updated_at
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar abate: {str(e)}")


@router.put("/{abate_id}", response_model=dict)
async def update_abate_completo(
    abate_id: str,
    abate_update: AbateCompletoUpdate,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Atualizar abate completo"""
    if db is None:
        raise HTTPException(status_code=500, detail="Erro de conexão com o banco de dados")
    
    crud = get_abate_completo_crud(db)
    try:
        abate = await crud.update(abate_id, abate_update)
        if not abate:
            raise HTTPException(status_code=404, detail="Abate não encontrado")
        
        return {
            "id": str(abate.id),
            "data_abate": abate.data_abate,
            "quantidade_aves": abate.quantidade_aves,
            "valor_kg_vivo": abate.valor_kg_vivo,
            "peso_total_kg": abate.peso_total_kg,
            "peso_medio_ave": abate.peso_medio_ave,
            "valor_total": abate.valor_total,
            "unidade": abate.unidade,
            "tipo_ave": abate.tipo_ave,
            "observacoes": abate.observacoes,
            "horarios": abate.horarios.model_dump(),
            "produtos": [produto.model_dump() for produto in abate.produtos],
            "despesas_fixas": abate.despesas_fixas.model_dump(),
            "peso_inteiro_abatido": abate.peso_inteiro_abatido,
            "preco_venda_kg": abate.preco_venda_kg,
            "created_at": abate.created_at,
            "updated_at": abate.updated_at
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar abate: {str(e)}")


@router.delete("/{abate_id}", response_model=dict)
async def delete_abate_completo(
    abate_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Deletar abate completo"""
    if db is None:
        raise HTTPException(status_code=500, detail="Erro de conexão com o banco de dados")
    
    crud = get_abate_completo_crud(db)
    try:
        success = await crud.delete(abate_id)
        if not success:
            raise HTTPException(status_code=404, detail="Abate não encontrado")
        
        return {"message": "Abate deletado com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar abate: {str(e)}")