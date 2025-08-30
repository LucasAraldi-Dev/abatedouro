import asyncio
import sys
sys.path.append('.')

from motor.motor_asyncio import AsyncIOMotorClient
from app.core.db import get_db
from app.crud.lote_abate import get_lote_abate_crud
from app.core.config import settings

async def debug_endpoint():
    try:
        print(f"Configurações:")
        print(f"  MONGODB_URI: {settings.MONGODB_URI}")
        print(f"  MONGODB_DBNAME: {settings.MONGODB_DBNAME}")
        
        # Testar get_db
        print("\nTestando get_db()...")
        db = await get_db()
        if db is None:
            print("✗ get_db() retornou None")
            return
        print(f"✓ get_db() funcionou: {db.name}")
        
        # Testar CRUD
        print("\nTestando get_lote_abate_crud()...")
        crud = get_lote_abate_crud(db)
        print(f"✓ CRUD criado: {type(crud)}")
        
        # Testar get_multi
        print("\nTestando crud.get_multi()...")
        lotes = await crud.get_multi(skip=0, limit=10)
        print(f"✓ get_multi funcionou: {len(lotes)} lotes encontrados")
        
        for lote in lotes:
            print(f"  - ID: {lote.id}, Unidade: {lote.unidade}")
            
    except Exception as e:
        print(f"✗ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_endpoint())