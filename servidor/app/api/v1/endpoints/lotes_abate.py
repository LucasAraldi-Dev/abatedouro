from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, Depends
from app.models.lote_abate import LoteAbate, LoteAbateCreate, LoteAbateUpdate
from app.crud.lote_abate import get_lote_abate_crud, CRUDLoteAbate
from app.core.db import get_db
from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter()


@router.post("/", response_model=dict, status_code=201)
async def create_lote_abate(
    lote_data: LoteAbateCreate,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Criar um novo lote de abate"""
    if db is None:
        raise HTTPException(status_code=500, detail="Erro de conexão com o banco de dados")
    
    crud = get_lote_abate_crud(db)
    try:
        lote = await crud.create(lote_data)
        return {
            "id": str(lote.id),
            "data_abate": lote.data_abate,
            "quantidade_aves": lote.quantidade_aves,
            "peso_total_kg": lote.peso_total_kg,
            "unidade": lote.unidade,
            "tipo_ave": lote.tipo_ave,
            "observacoes": lote.observacoes,
            "created_at": lote.created_at,
            "updated_at": lote.updated_at
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar lote: {str(e)}")


@router.get("/", response_model=List[dict])
async def list_lotes_abate(
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(100, ge=1, le=1000, description="Limite de registros por página"),
    unidade: Optional[str] = Query(None, description="Filtrar por unidade"),
    tipo_ave: Optional[str] = Query(None, description="Filtrar por tipo de ave"),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Listar lotes de abate com filtros opcionais"""
    if db is None:
        raise HTTPException(status_code=500, detail="Erro de conexão com o banco de dados")
    
    crud = get_lote_abate_crud(db)
    try:
        # Construir filtros
        filters = {}
        if unidade:
            filters["unidade"] = {"$regex": unidade, "$options": "i"}
        if tipo_ave:
            filters["tipo_ave"] = tipo_ave
        
        # Buscar lotes com filtros e paginação
        lotes = await crud.get_multi(skip=skip, limit=limit, filters=filters)
        
        # Converter para formato de resposta
        result = []
        for lote in lotes:
            result.append({
                "id": str(lote.id),
                "data_abate": lote.data_abate,
                "quantidade_aves": lote.quantidade_aves,
                "peso_total_kg": lote.peso_total_kg,
                "unidade": lote.unidade,
                "tipo_ave": lote.tipo_ave,
                "observacoes": lote.observacoes,
                "created_at": lote.created_at,
                "updated_at": lote.updated_at
            })
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar lotes: {str(e)}")


@router.get("/count", response_model=dict)
async def count_lotes_abate(
    unidade: Optional[str] = Query(None, description="Filtrar por unidade"),
    tipo_ave: Optional[str] = Query(None, description="Filtrar por tipo de ave"),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Contar total de lotes de abate"""
    if db is None:
        raise HTTPException(status_code=500, detail="Erro de conexão com o banco de dados")
    
    crud = get_lote_abate_crud(db)
    try:
        total = await crud.count(unidade=unidade, tipo_ave=tipo_ave)
        return {"total": total}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao contar lotes: {str(e)}")


@router.get("/periodo", response_model=List[dict])
async def get_lotes_by_period(
    start_date: datetime = Query(..., description="Data inicial (ISO format)"),
    end_date: datetime = Query(..., description="Data final (ISO format)"),
    unidade: Optional[str] = Query(None, description="Filtrar por unidade"),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Buscar lotes por período"""
    if start_date > end_date:
        raise HTTPException(
            status_code=400, 
            detail="Data inicial deve ser anterior à data final"
        )
    
    if db is None:
        raise HTTPException(status_code=500, detail="Erro de conexão com o banco de dados")
    
    crud = get_lote_abate_crud(db)
    try:
        # Construir filtros para período
        filters = {
            "data_abate": {
                "$gte": start_date.date(),
                "$lte": end_date.date()
            }
        }
        
        if unidade:
            filters["unidade"] = unidade
        
        # Buscar lotes no período
        lotes = await crud.get_multi(filters=filters)
        
        # Converter para formato de resposta
        result = []
        for lote in lotes:
            result.append({
                "id": str(lote.id),
                "data_abate": lote.data_abate,
                "quantidade_aves": lote.quantidade_aves,
                "peso_total_kg": lote.peso_total_kg,
                "unidade": lote.unidade,
                "tipo_ave": lote.tipo_ave,
                "observacoes": lote.observacoes,
                "created_at": lote.created_at,
                "updated_at": lote.updated_at
            })
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar lotes por período: {str(e)}")


@router.get("/{lote_id}", response_model=dict)
async def get_lote_abate(
    lote_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Buscar lotes de abate por período"""
    if db is None:
        raise HTTPException(status_code=500, detail="Erro de conexão com o banco de dados")
    
    crud = get_lote_abate_crud(db)
    try:
        lote = await crud.get(lote_id)
        if not lote:
            raise HTTPException(status_code=404, detail="Lote de abate não encontrado")
        
        return {
            "id": str(lote.id),
            "data_abate": lote.data_abate,
            "quantidade_aves": lote.quantidade_aves,
            "peso_total_kg": lote.peso_total_kg,
            "unidade": lote.unidade,
            "tipo_ave": lote.tipo_ave,
            "observacoes": lote.observacoes,
            "created_at": lote.created_at,
            "updated_at": lote.updated_at
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar lote: {str(e)}")


@router.put("/{lote_id}", response_model=dict)
async def update_lote_abate(
    lote_id: str,
    lote_update: LoteAbateUpdate,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Buscar lote de abate por ID"""
    if db is None:
        raise HTTPException(status_code=500, detail="Erro de conexão com o banco de dados")
    
    crud = get_lote_abate_crud(db)
    try:
        lote = await crud.update(lote_id, lote_update)
        if not lote:
            raise HTTPException(status_code=404, detail="Lote de abate não encontrado")
        
        return {
            "id": str(lote.id),
            "data_abate": lote.data_abate,
            "quantidade_aves": lote.quantidade_aves,
            "peso_total_kg": lote.peso_total_kg,
            "unidade": lote.unidade,
            "tipo_ave": lote.tipo_ave,
            "observacoes": lote.observacoes,
            "created_at": lote.created_at,
            "updated_at": lote.updated_at
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar lote: {str(e)}")


@router.delete("/{lote_id}", response_model=dict)
async def delete_lote_abate(
    lote_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Atualizar lote de abate"""
    if db is None:
        raise HTTPException(status_code=500, detail="Erro de conexão com o banco de dados")
    
    crud = get_lote_abate_crud(db)
    try:
        success = await crud.delete(lote_id)
        if not success:
            raise HTTPException(status_code=404, detail="Lote de abate não encontrado")
        
        return {"message": "Lote de abate excluído com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao excluir lote: {str(e)}")