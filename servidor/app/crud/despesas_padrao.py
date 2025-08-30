from typing import Optional
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection
from bson import ObjectId
from datetime import datetime

from app.models.despesas_padrao import DespesasPadrao, DespesasPadraoCreate, DespesasPadraoUpdate

class CRUDDespesasPadrao:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection: AsyncIOMotorCollection = db.despesas_padrao
    
    async def get_default(self) -> Optional[DespesasPadrao]:
        """Buscar valores padrão das despesas (sempre o mais recente)"""
        despesa = await self.collection.find_one({}, sort=[("updated_at", -1)])
        if despesa:
            despesa["id"] = str(despesa["_id"])
            return DespesasPadrao(**despesa)
        return None
    
    async def create_or_update(self, despesas_data: DespesasPadraoCreate) -> DespesasPadrao:
        """Criar ou atualizar valores padrão das despesas"""
        # Verificar se já existe um registro
        existing = await self.collection.find_one({})
        
        despesas_dict = despesas_data.dict()
        despesas_dict["updated_at"] = datetime.now()
        
        if existing:
            # Atualizar registro existente
            await self.collection.update_one(
                {"_id": existing["_id"]},
                {"$set": despesas_dict}
            )
            updated_despesa = await self.collection.find_one({"_id": existing["_id"]})
            updated_despesa["id"] = str(updated_despesa["_id"])
            return DespesasPadrao(**updated_despesa)
        else:
            # Criar novo registro
            despesas_dict["created_at"] = datetime.now()
            result = await self.collection.insert_one(despesas_dict)
            created_despesa = await self.collection.find_one({"_id": result.inserted_id})
            created_despesa["id"] = str(created_despesa["_id"])
            return DespesasPadrao(**created_despesa)
    
    async def update(self, despesas_update: DespesasPadraoUpdate) -> Optional[DespesasPadrao]:
        """Atualizar valores padrão das despesas"""
        existing = await self.collection.find_one({})
        if not existing:
            return None
        
        update_data = {k: v for k, v in despesas_update.dict().items() if v is not None}
        update_data["updated_at"] = datetime.now()
        
        await self.collection.update_one(
            {"_id": existing["_id"]},
            {"$set": update_data}
        )
        
        updated_despesa = await self.collection.find_one({"_id": existing["_id"]})
        updated_despesa["id"] = str(updated_despesa["_id"])
        return DespesasPadrao(**updated_despesa)
    
    async def delete(self) -> bool:
        """Deletar valores padrão das despesas"""
        result = await self.collection.delete_many({})
        return result.deleted_count > 0

def get_despesas_padrao_crud(db: AsyncIOMotorDatabase) -> CRUDDespesasPadrao:
    """Factory function para criar instância do CRUD"""
    return CRUDDespesasPadrao(db)