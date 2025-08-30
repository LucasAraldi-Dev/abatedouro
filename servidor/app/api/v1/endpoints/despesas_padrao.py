from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional

from app.core.db import get_db
from app.crud.despesas_padrao import get_despesas_padrao_crud
from app.models.despesas_padrao import DespesasPadrao, DespesasPadraoCreate, DespesasPadraoUpdate
from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter()

@router.get("/", response_model=Optional[DespesasPadrao])
async def get_despesas_padrao(
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Buscar valores padrão das despesas"""
    try:
        crud = get_despesas_padrao_crud(db)
        despesas = await crud.get_default()
        return despesas
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar despesas padrão: {str(e)}"
        )

@router.post("/", response_model=DespesasPadrao)
async def create_or_update_despesas_padrao(
    despesas_data: DespesasPadraoCreate,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Criar ou atualizar valores padrão das despesas"""
    try:
        crud = get_despesas_padrao_crud(db)
        despesas = await crud.create_or_update(despesas_data)
        return despesas
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao salvar despesas padrão: {str(e)}"
        )

@router.put("/", response_model=Optional[DespesasPadrao])
async def update_despesas_padrao(
    despesas_update: DespesasPadraoUpdate,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Atualizar valores padrão das despesas"""
    try:
        crud = get_despesas_padrao_crud(db)
        despesas = await crud.update(despesas_update)
        if not despesas:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Despesas padrão não encontradas"
            )
        return despesas
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar despesas padrão: {str(e)}"
        )

@router.delete("/")
async def delete_despesas_padrao(
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Deletar valores padrão das despesas"""
    try:
        crud = get_despesas_padrao_crud(db)
        deleted = await crud.delete()
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Despesas padrão não encontradas"
            )
        return {"message": "Despesas padrão deletadas com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao deletar despesas padrão: {str(e)}"
        )