from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime

from app.core.db import get_db
from app.crud.produto import get_produto_crud
from app.models.produto import Produto, ProdutoCreate, ProdutoUpdate
from app.api.v1.endpoints.produto_log import criar_log_alteracao_produto

router = APIRouter()


@router.post("/", response_model=Produto, status_code=201)
async def create_produto(
    produto_data: ProdutoCreate,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Criar um novo produto/corte"""
    crud = get_produto_crud(db)
    return await crud.create(produto_data)


@router.get("/", response_model=List[Produto])
async def list_produtos(
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(100, ge=1, le=1000, description="Limite de registros por página"),
    search: Optional[str] = Query(None, description="Buscar por nome, tipo ou categoria"),
    tipo: Optional[str] = Query(None, description="Filtrar por tipo de produto"),
    unidade_origem: Optional[str] = Query(None, description="Filtrar por unidade de origem"),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Listar produtos/cortes com filtros opcionais"""
    crud = get_produto_crud(db)
    return await crud.get_multi(
        skip=skip, 
        limit=limit,
        search=search,
        tipo=tipo, 
        unidade_origem=unidade_origem
    )


@router.get("/count", response_model=dict)
async def count_produtos(
    tipo: Optional[str] = Query(None, description="Filtrar por tipo de produto"),
    unidade_origem: Optional[str] = Query(None, description="Filtrar por unidade de origem"),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Contar total de produtos/cortes"""
    crud = get_produto_crud(db)
    total = await crud.count(tipo=tipo, unidade_origem=unidade_origem)
    return {"total": total}


@router.get("/tipo/{tipo}", response_model=List[Produto])
async def get_produtos_by_tipo(
    tipo: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Buscar produtos por tipo específico"""
    crud = get_produto_crud(db)
    return await crud.get_by_tipo(tipo)


@router.get("/preco", response_model=List[Produto])
async def get_produtos_by_price_range(
    min_price: float = Query(..., ge=0, description="Preço mínimo por kg"),
    max_price: float = Query(..., ge=0, description="Preço máximo por kg"),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Buscar produtos por faixa de preço"""
    if min_price > max_price:
        raise HTTPException(
            status_code=400, 
            detail="Preço mínimo deve ser menor que o preço máximo"
        )
    
    crud = get_produto_crud(db)
    return await crud.get_price_range(min_price, max_price)


@router.get("/{produto_id}", response_model=Produto)
async def get_produto(
    produto_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Buscar produto/corte por ID"""
    crud = get_produto_crud(db)
    produto = await crud.get(produto_id)
    
    if not produto:
        raise HTTPException(
            status_code=404, 
            detail="Produto não encontrado"
        )
    
    return produto


@router.put("/{produto_id}", response_model=Produto)
async def update_produto(
    produto_id: str,
    produto_update: ProdutoUpdate,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Atualizar produto/corte existente"""
    crud = get_produto_crud(db)
    
    # Verificar se o produto existe
    existing_produto = await crud.get(produto_id)
    if not existing_produto:
        raise HTTPException(
            status_code=404, 
            detail="Produto não encontrado"
        )
    
    # Verificar se houve alteração no preço para criar log
    if produto_update.preco_kg is not None and produto_update.preco_kg != existing_produto.preco_kg:
        await criar_log_alteracao_produto(
            db=db,
            produto_id=produto_id,
            tipo_alteracao="Edição",
            campo_alterado="preco_kg",
            valor_anterior=str(existing_produto.preco_kg),
            valor_novo=str(produto_update.preco_kg),
            usuario="Sistema"  # Pode ser alterado para receber o usuário logado
        )
    
    updated_produto = await crud.update(produto_id, produto_update)
    return updated_produto


@router.delete("/{produto_id}", status_code=204)
async def delete_produto(
    produto_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Deletar produto/corte"""
    crud = get_produto_crud(db)
    
    # Verificar se o produto existe
    existing_produto = await crud.get(produto_id)
    if not existing_produto:
        raise HTTPException(
            status_code=404, 
            detail="Produto não encontrado"
        )
    
    success = await crud.delete(produto_id)
    if not success:
        raise HTTPException(
            status_code=500, 
            detail="Erro ao deletar produto"
        )


@router.patch("/{produto_id}/preco", response_model=Produto)
async def update_produto_preco(
    produto_id: str,
    novo_preco: float = Query(..., ge=0, description="Novo preço por kg"),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Atualizar apenas o preço de um produto/corte"""
    crud = get_produto_crud(db)
    
    # Verificar se o produto existe
    existing_produto = await crud.get(produto_id)
    if not existing_produto:
        raise HTTPException(
            status_code=404, 
            detail="Produto não encontrado"
        )
    
    # Criar log da alteração de preço
    await criar_log_alteracao_produto(
        db=db,
        produto_id=produto_id,
        tipo_alteracao="Atualização de Preço",
        campo_alterado="preco_kg",
        valor_anterior=str(existing_produto.preco_kg),
        valor_novo=str(novo_preco),
        usuario="Sistema"  # Pode ser alterado para receber o usuário logado
    )
    
    # Atualizar apenas o preço
    produto_update = ProdutoUpdate(preco_kg=novo_preco)
    updated_produto = await crud.update(produto_id, produto_update)
    return updated_produto