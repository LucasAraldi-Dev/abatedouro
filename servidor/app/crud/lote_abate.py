from datetime import datetime
from typing import List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import DESCENDING

from app.models.lote_abate import LoteAbate, LoteAbateCreate, LoteAbateUpdate


class CRUDLoteAbate:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.lotes_abate

    async def create(self, lote_data: LoteAbateCreate) -> LoteAbate:
        """Criar um novo lote de abate"""
        lote_dict = lote_data.dict()
        lote_dict["created_at"] = datetime.utcnow()
        lote_dict["updated_at"] = None
        
        result = await self.collection.insert_one(lote_dict)
        created_lote = await self.collection.find_one({"_id": result.inserted_id})
        return LoteAbate(**created_lote)

    async def get(self, lote_id: str) -> Optional[LoteAbate]:
        """Buscar lote por ID"""
        if not ObjectId.is_valid(lote_id):
            return None
            
        lote = await self.collection.find_one({"_id": ObjectId(lote_id)})
        if lote:
            return LoteAbate(**lote)
        return None

    async def get_multi(
        self, *, skip: int = 0, limit: int = 100, filters: Optional[dict] = None
    ) -> List[LoteAbate]:
        """Retrieve multiple lotes de abate with pagination and filters"""
        query = filters or {}
        cursor = self.collection.find(query).skip(skip).limit(limit)
        lotes = await cursor.to_list(length=limit)
        return [LoteAbate(**lote) for lote in lotes]

    async def update(self, lote_id: str, lote_update: LoteAbateUpdate) -> Optional[LoteAbate]:
        """Atualizar lote existente"""
        if not ObjectId.is_valid(lote_id):
            return None
            
        update_data = lote_update.dict(exclude_unset=True)
        if update_data:
            update_data["updated_at"] = datetime.utcnow()
            
            await self.collection.update_one(
                {"_id": ObjectId(lote_id)},
                {"$set": update_data}
            )
            
        updated_lote = await self.collection.find_one({"_id": ObjectId(lote_id)})
        if updated_lote:
            return LoteAbate(**updated_lote)
        return None

    async def delete(self, lote_id: str) -> bool:
        """Deletar lote por ID"""
        if not ObjectId.is_valid(lote_id):
            return False
            
        result = await self.collection.delete_one({"_id": ObjectId(lote_id)})
        return result.deleted_count > 0

    async def count(self, unidade: Optional[str] = None, tipo_ave: Optional[str] = None) -> int:
        """Contar total de lotes com filtros opcionais"""
        query = {}
        
        if unidade:
            query["unidade"] = {"$regex": unidade, "$options": "i"}
        if tipo_ave:
            query["tipo_ave"] = tipo_ave
            
        return await self.collection.count_documents(query)

    async def get_by_date_range(
        self, 
        start_date: datetime, 
        end_date: datetime,
        unidade: Optional[str] = None
    ) -> List[LoteAbate]:
        """Buscar lotes por período"""
        query = {
            "data_abate": {
                "$gte": start_date,
                "$lte": end_date
            }
        }
        
        if unidade:
            query["unidade"] = {"$regex": unidade, "$options": "i"}
            
        cursor = self.collection.find(query).sort("data_abate", DESCENDING)
        lotes = await cursor.to_list(length=None)
        return [LoteAbate(**lote) for lote in lotes]


def get_lote_abate_crud(db: AsyncIOMotorDatabase) -> CRUDLoteAbate:
    """Factory function para criar instância do CRUD"""
    return CRUDLoteAbate(db)