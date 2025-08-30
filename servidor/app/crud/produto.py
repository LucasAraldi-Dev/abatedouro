from datetime import datetime
from typing import List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import DESCENDING

from app.models.produto import Produto, ProdutoCreate, ProdutoUpdate


class CRUDProduto:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.produtos

    async def create(self, produto_data: ProdutoCreate) -> Produto:
        """Criar um novo produto"""
        produto_dict = produto_data.dict()
        produto_dict["created_at"] = datetime.utcnow()
        produto_dict["updated_at"] = None
        
        result = await self.collection.insert_one(produto_dict)
        created_produto = await self.collection.find_one({"_id": result.inserted_id})
        return Produto(**created_produto)

    async def get(self, produto_id: str) -> Optional[Produto]:
        """Buscar produto por ID"""
        if not ObjectId.is_valid(produto_id):
            return None
            
        produto = await self.collection.find_one({"_id": ObjectId(produto_id)})
        if produto:
            return Produto(**produto)
        return None

    async def get_multi(
        self, 
        skip: int = 0, 
        limit: int = 100,
        search: Optional[str] = None,
        tipo: Optional[str] = None,
        unidade_origem: Optional[str] = None
    ) -> List[Produto]:
        """Listar produtos com filtros opcionais"""
        query = {}
        
        # Busca por texto em nome e tipo
        if search:
            query["$or"] = [
                {"nome": {"$regex": search, "$options": "i"}},
                {"tipo": {"$regex": search, "$options": "i"}}
            ]
        
        if tipo:
            query["tipo"] = {"$regex": tipo, "$options": "i"}
        if unidade_origem:
            query["unidade_origem"] = {"$regex": unidade_origem, "$options": "i"}
            
        cursor = self.collection.find(query).sort("nome", 1).skip(skip).limit(limit)
        produtos = await cursor.to_list(length=limit)
        return [Produto(**produto) for produto in produtos]

    async def update(self, produto_id: str, produto_update: ProdutoUpdate) -> Optional[Produto]:
        """Atualizar produto existente"""
        if not ObjectId.is_valid(produto_id):
            return None
            
        update_data = produto_update.dict(exclude_unset=True)
        if update_data:
            update_data["updated_at"] = datetime.utcnow()
            
            await self.collection.update_one(
                {"_id": ObjectId(produto_id)},
                {"$set": update_data}
            )
            
        updated_produto = await self.collection.find_one({"_id": ObjectId(produto_id)})
        if updated_produto:
            return Produto(**updated_produto)
        return None

    async def delete(self, produto_id: str) -> bool:
        """Deletar produto por ID"""
        if not ObjectId.is_valid(produto_id):
            return False
            
        result = await self.collection.delete_one({"_id": ObjectId(produto_id)})
        return result.deleted_count > 0

    async def count(self, tipo: Optional[str] = None, unidade_origem: Optional[str] = None) -> int:
        """Contar total de produtos com filtros opcionais"""
        query = {}
        
        if tipo:
            query["tipo"] = {"$regex": tipo, "$options": "i"}
        if unidade_origem:
            query["unidade_origem"] = {"$regex": unidade_origem, "$options": "i"}
            
        return await self.collection.count_documents(query)

    async def get_by_tipo(self, tipo: str) -> List[Produto]:
        """Buscar produtos por tipo"""
        query = {"tipo": {"$regex": tipo, "$options": "i"}}
        cursor = self.collection.find(query).sort("nome", 1)
        produtos = await cursor.to_list(length=None)
        return [Produto(**produto) for produto in produtos]

    async def get_price_range(self, min_price: float, max_price: float) -> List[Produto]:
        """Buscar produtos por faixa de preço"""
        query = {
            "preco_kg": {
                "$gte": min_price,
                "$lte": max_price
            }
        }
        cursor = self.collection.find(query).sort("preco_kg", 1)
        produtos = await cursor.to_list(length=None)
        return [Produto(**produto) for produto in produtos]


def get_produto_crud(db: AsyncIOMotorDatabase) -> CRUDProduto:
    """Factory function para criar instância do CRUD"""
    return CRUDProduto(db)