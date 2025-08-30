from fastapi import APIRouter, HTTPException, Depends
from typing import List
from bson import ObjectId
from datetime import datetime

from app.models.produto_log import ProdutoLogCreate, ProdutoLogResponse
from app.core.db import get_db

router = APIRouter()


@router.post("/", response_model=ProdutoLogResponse)
async def criar_log_produto(log: ProdutoLogCreate, db=Depends(get_db)):
    """
    Criar um novo log de alteração de produto
    """
    try:
        log_dict = log.dict()
        log_dict["data_alteracao"] = datetime.now()
        
        result = await db.produto_logs.insert_one(log_dict)
        
        if result.inserted_id:
            created_log = await db.produto_logs.find_one({"_id": result.inserted_id})
            if created_log:
                created_log["id"] = str(created_log["_id"])
                created_log["produto_id"] = str(created_log["produto_id"])
                return ProdutoLogResponse(**created_log)
        
        raise HTTPException(status_code=500, detail="Erro ao criar log")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@router.get("/produto/{produto_id}", response_model=List[ProdutoLogResponse])
async def get_historico_produto(produto_id: str, db=Depends(get_db)):
    """
    Obter histórico de alterações de um produto específico
    """
    try:
        if not ObjectId.is_valid(produto_id):
            raise HTTPException(status_code=400, detail="ID do produto inválido")
        
        logs = await db.produto_logs.find(
            {"produto_id": ObjectId(produto_id)}
        ).sort("data_alteracao", -1).to_list(length=None)
        
        logs_response = []
        for log in logs:
            log["id"] = str(log["_id"])
            log["produto_id"] = str(log["produto_id"])
            logs_response.append(ProdutoLogResponse(**log))
        
        return logs_response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@router.get("/", response_model=List[ProdutoLogResponse])
async def listar_todos_logs(limit: int = 100, db=Depends(get_db)):
    """
    Listar todos os logs de alterações de produtos
    """
    try:
        logs = await db.produto_logs.find().sort("data_alteracao", -1).limit(limit).to_list(length=None)
        
        logs_response = []
        for log in logs:
            log["id"] = str(log["_id"])
            log["produto_id"] = str(log["produto_id"])
            logs_response.append(ProdutoLogResponse(**log))
        
        return logs_response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


async def criar_log_alteracao_produto(
    db,
    produto_id: str,
    tipo_alteracao: str,
    campo_alterado: str,
    valor_anterior: str,
    valor_novo: str,
    usuario: str = "Sistema",
    observacoes: str = None
):
    """
    Função auxiliar para criar logs de alteração
    """
    try:
        log_data = {
            "produto_id": ObjectId(produto_id),
            "tipo_alteracao": tipo_alteracao,
            "campo_alterado": campo_alterado,
            "valor_anterior": valor_anterior,
            "valor_novo": valor_novo,
            "data_alteracao": datetime.now(),
            "usuario": usuario,
            "observacoes": observacoes
        }
        
        await db.produto_logs.insert_one(log_data)
        return True
    except Exception as e:
        print(f"Erro ao criar log: {str(e)}")
        return False