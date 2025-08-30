import asyncio
import sys
sys.path.append('.')

from motor.motor_asyncio import AsyncIOMotorClient
from app.crud.lote_abate import CRUDLoteAbate
from app.core.config import settings

async def test_lotes_endpoint():
    try:
        # Conectar ao MongoDB
        client = AsyncIOMotorClient(settings.MONGODB_URI)
        db = client[settings.MONGODB_DBNAME]
        
        # Testar conexão
        await client.admin.command('ping')
        print("✓ MongoDB conectado com sucesso")
        
        # Criar instância do CRUD
        crud = CRUDLoteAbate(db)
        
        # Testar busca de lotes
        lotes = await crud.get_multi(skip=0, limit=10)
        print(f"✓ Encontrados {len(lotes)} lotes")
        
        for lote in lotes:
            print(f"  - ID: {lote.id}, Unidade: {lote.unidade}")
            
    except Exception as e:
        print(f"✗ Erro: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if 'client' in locals():
            client.close()

if __name__ == "__main__":
    asyncio.run(test_lotes_endpoint())