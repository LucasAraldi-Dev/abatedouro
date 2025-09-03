from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional

from app.core.db import get_db
from app.crud.configuracao_limites import get_configuracao_limites_crud
from app.models.configuracao_limites import ConfiguracaoLimites, ConfiguracaoLimitesCreate, ConfiguracaoLimitesUpdate
from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter()

@router.get("/", response_model=Optional[ConfiguracaoLimites])
async def get_configuracao_limites(
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Buscar configuração de limites e alertas"""
    try:
        crud = get_configuracao_limites_crud(db)
        config = await crud.get_default()
        return config
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar configuração de limites: {str(e)}"
        )

@router.post("/", response_model=ConfiguracaoLimites)
async def create_or_update_configuracao_limites(
    config_data: ConfiguracaoLimitesCreate,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Criar ou atualizar configuração de limites e alertas"""
    try:
        crud = get_configuracao_limites_crud(db)
        config = await crud.create_or_update(config_data)
        return config
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao salvar configuração de limites: {str(e)}"
        )

@router.put("/", response_model=Optional[ConfiguracaoLimites])
async def update_configuracao_limites(
    config_update: ConfiguracaoLimitesUpdate,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Atualizar configuração de limites e alertas"""
    try:
        crud = get_configuracao_limites_crud(db)
        config = await crud.update(config_update)
        if not config:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Configuração de limites não encontrada"
            )
        return config
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar configuração de limites: {str(e)}"
        )

@router.delete("/")
async def delete_configuracao_limites(
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Deletar configuração de limites e alertas"""
    try:
        crud = get_configuracao_limites_crud(db)
        deleted = await crud.delete()
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Configuração de limites não encontrada"
            )
        return {"message": "Configuração de limites deletada com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao deletar configuração de limites: {str(e)}"
        )