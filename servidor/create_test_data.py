import asyncio
import sys
sys.path.append('.')

from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from app.crud.lote_abate import CRUDLoteAbate
from app.models.lote_abate import LoteAbateCreate
from app.core.config import settings

async def create_test_data():
    try:
        # Conectar ao MongoDB
        client = AsyncIOMotorClient(settings.MONGODB_URI)
        db = client[settings.MONGODB_DBNAME]
        
        # Testar conexão
        await client.admin.command('ping')
        print("✓ MongoDB conectado com sucesso")
        
        # Criar instância do CRUD
        crud = CRUDLoteAbate(db)
        
        # Criar dados de teste
        test_lotes = [
            LoteAbateCreate(
                data_abate=datetime(2025, 1, 15, 8, 0, 0),
                quantidade_aves=15000,
                peso_total_kg=28500.0,
                unidade="Unidade A",
                tipo_ave="Frango",
                observacoes="Lote de teste 1"
            ),
            LoteAbateCreate(
                data_abate=datetime(2025, 1, 14, 8, 0, 0),
                quantidade_aves=12000,
                peso_total_kg=22800.0,
                unidade="Unidade B",
                tipo_ave="Frango",
                observacoes="Lote de teste 2"
            )
        ]
        
        # Inserir dados de teste
        for lote_data in test_lotes:
            lote = await crud.create(lote_data)
            print(f"✓ Criado lote: {lote.id} - {lote.unidade}")
            
        print("✓ Dados de teste criados com sucesso")
            
    except Exception as e:
        print(f"✗ Erro: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if 'client' in locals():
            client.close()

if __name__ == "__main__":
    asyncio.run(create_test_data())