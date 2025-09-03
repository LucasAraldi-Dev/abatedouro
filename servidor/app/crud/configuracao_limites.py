from typing import Optional
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection
from bson import ObjectId
from datetime import datetime

from app.models.configuracao_limites import ConfiguracaoLimites, ConfiguracaoLimitesCreate, ConfiguracaoLimitesUpdate

class CRUDConfiguracaoLimites:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection: AsyncIOMotorCollection = db.configuracao_limites
    
    async def get_default(self) -> Optional[ConfiguracaoLimites]:
        """Buscar configuração de limites (sempre a mais recente)"""
        config = await self.collection.find_one({}, sort=[("updated_at", -1)])
        if config:
            config["id"] = str(config["_id"])
            return ConfiguracaoLimites(**config)
        return None
    
    async def create_or_update(self, config_data: ConfiguracaoLimitesCreate) -> ConfiguracaoLimites:
        """Criar ou atualizar configuração de limites"""
        # Verificar se já existe um registro
        existing = await self.collection.find_one({})
        
        config_dict = config_data.dict()
        config_dict["updated_at"] = datetime.now()
        
        if existing:
            # Atualizar registro existente
            await self.collection.update_one(
                {"_id": existing["_id"]},
                {"$set": config_dict}
            )
            updated_config = await self.collection.find_one({"_id": existing["_id"]})
            updated_config["id"] = str(updated_config["_id"])
            return ConfiguracaoLimites(**updated_config)
        else:
            # Criar novo registro
            config_dict["created_at"] = datetime.now()
            result = await self.collection.insert_one(config_dict)
            created_config = await self.collection.find_one({"_id": result.inserted_id})
            created_config["id"] = str(created_config["_id"])
            return ConfiguracaoLimites(**created_config)
    
    async def update(self, config_update: ConfiguracaoLimitesUpdate) -> Optional[ConfiguracaoLimites]:
        """Atualizar configuração de limites"""
        existing = await self.collection.find_one({})
        if not existing:
            return None
        
        update_data = {k: v for k, v in config_update.dict().items() if v is not None}
        update_data["updated_at"] = datetime.now()
        
        await self.collection.update_one(
            {"_id": existing["_id"]},
            {"$set": update_data}
        )
        
        updated_config = await self.collection.find_one({"_id": existing["_id"]})
        updated_config["id"] = str(updated_config["_id"])
        return ConfiguracaoLimites(**updated_config)
    
    async def delete(self) -> bool:
        """Deletar configuração de limites"""
        result = await self.collection.delete_many({})
        return result.deleted_count > 0

def get_configuracao_limites_crud(db: AsyncIOMotorDatabase) -> CRUDConfiguracaoLimites:
    """Factory function para criar instância do CRUD"""
    return CRUDConfiguracaoLimites(db)