from typing import List, Optional, Dict, Any
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from ..models.abate_completo import (
    AbateCompleto,
    AbateCompletoCreate,
    AbateCompletoUpdate,
    AbateCompletoInDB
)
from ..core.db import get_collection
from ..services.metrics_calculator import MetricsCalculator


class AbateCompletoCRUD:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = get_collection(db, "abates_completos")

    async def create(self, abate_data: AbateCompletoCreate) -> AbateCompleto:
        """Criar um novo abate completo"""
        abate_dict = abate_data.model_dump()
        abate_dict["created_at"] = datetime.utcnow()
        abate_dict["updated_at"] = None
        
        # Calcular métricas automaticamente
        calculator = MetricsCalculator()
        metricas = calculator.calcular_metricas_completas(abate_dict)
        abate_dict.update(metricas)
        
        result = await self.collection.insert_one(abate_dict)
        abate_dict["_id"] = result.inserted_id
        
        return AbateCompleto(**abate_dict)

    async def get(self, abate_id: str) -> Optional[AbateCompleto]:
        """Buscar abate completo por ID"""
        if not ObjectId.is_valid(abate_id):
            return None
            
        abate_data = await self.collection.find_one({"_id": ObjectId(abate_id)})
        if abate_data:
            return AbateCompleto(**abate_data)
        return None

    async def get_many(
        self,
        skip: int = 0,
        limit: int = 100,
        unidade: Optional[str] = None,
        tipo_ave: Optional[str] = None,
        data_inicio: Optional[datetime] = None,
        data_fim: Optional[datetime] = None
    ) -> List[AbateCompleto]:
        """Buscar múltiplos abates completos com filtros"""
        query = {}
        
        if unidade:
            query["unidade"] = {"$regex": unidade, "$options": "i"}
        if tipo_ave:
            query["tipo_ave"] = {"$regex": tipo_ave, "$options": "i"}
        if data_inicio or data_fim:
            date_query = {}
            if data_inicio:
                date_query["$gte"] = data_inicio
            if data_fim:
                date_query["$lte"] = data_fim
            query["data_abate"] = date_query
        
        cursor = self.collection.find(query).skip(skip).limit(limit).sort("data_abate", -1)
        abates = []
        
        async for abate_data in cursor:
            abates.append(AbateCompleto(**abate_data))
        
        return abates

    async def update(self, abate_id: str, abate_update: AbateCompletoUpdate) -> Optional[AbateCompleto]:
        """Atualizar abate completo"""
        if not ObjectId.is_valid(abate_id):
            return None
        
        update_data = abate_update.model_dump(exclude_unset=True)
        if update_data:
            # Buscar o documento atual para recalcular métricas
            current_doc = await self.collection.find_one({"_id": ObjectId(abate_id)})
            if not current_doc:
                return None
            
            # Mesclar dados atuais com atualizações
            merged_data = {**current_doc, **update_data}
            
            # Recalcular métricas se dados relevantes foram alterados
            relevant_fields = {
                'quantidade_aves', 'valor_kg_vivo', 'peso_total_kg', 'peso_medio_ave',
                'valor_total', 'produtos', 'despesas_fixas', 'horarios'
            }
            
            if any(field in update_data for field in relevant_fields):
                calculator = MetricsCalculator()
                metricas = calculator.calcular_metricas_completas(merged_data)
                update_data.update(metricas)
            
            update_data["updated_at"] = datetime.utcnow()
            
            result = await self.collection.update_one(
                {"_id": ObjectId(abate_id)},
                {"$set": update_data}
            )
            
            if result.modified_count:
                return await self.get(abate_id)
        
        return None

    async def delete(self, abate_id: str) -> bool:
        """Deletar abate completo"""
        if not ObjectId.is_valid(abate_id):
            return False
            
        result = await self.collection.delete_one({"_id": ObjectId(abate_id)})
        return result.deleted_count > 0

    async def count(
        self,
        unidade: Optional[str] = None,
        tipo_ave: Optional[str] = None,
        data_inicio: Optional[datetime] = None,
        data_fim: Optional[datetime] = None
    ) -> int:
        """Contar abates completos com filtros"""
        query = {}
        
        if unidade:
            query["unidade"] = {"$regex": unidade, "$options": "i"}
        if tipo_ave:
            query["tipo_ave"] = {"$regex": tipo_ave, "$options": "i"}
        if data_inicio or data_fim:
            date_query = {}
            if data_inicio:
                date_query["$gte"] = data_inicio
            if data_fim:
                date_query["$lte"] = data_fim
            query["data_abate"] = date_query
        
        return await self.collection.count_documents(query)

    async def get_by_periodo(
        self,
        data_inicio: datetime,
        data_fim: datetime,
        unidade: Optional[str] = None
    ) -> List[AbateCompleto]:
        """Buscar abates por período específico"""
        query = {
            "data_abate": {
                "$gte": data_inicio,
                "$lte": data_fim
            }
        }
        
        if unidade:
            query["unidade"] = {"$regex": unidade, "$options": "i"}
        
        cursor = self.collection.find(query).sort("data_abate", -1)
        abates = []
        
        async for abate_data in cursor:
            abates.append(AbateCompleto(**abate_data))
        
        return abates


def get_abate_completo_crud(db: AsyncIOMotorDatabase) -> AbateCompletoCRUD:
    """Factory function para criar instância do CRUD"""
    return AbateCompletoCRUD(db)