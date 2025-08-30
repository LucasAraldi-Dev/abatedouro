import asyncio
import sys
sys.path.append('.')

from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.db import get_db
from app.crud.lote_abate import get_lote_abate_crud
import json

async def test_serialization():
    try:
        # Conectar ao banco
        db = await get_db()
        crud = get_lote_abate_crud(db)
        
        # Buscar lotes
        lotes = await crud.get_multi(skip=0, limit=10)
        print(f"Encontrados {len(lotes)} lotes")
        
        # Testar serialização como no endpoint
        result = []
        for lote in lotes:
            print(f"\nProcessando lote {lote.id}:")
            print(f"  data_abate: {lote.data_abate} (tipo: {type(lote.data_abate)})")
            print(f"  created_at: {lote.created_at} (tipo: {type(lote.created_at)})")
            print(f"  updated_at: {lote.updated_at} (tipo: {type(lote.updated_at)})")
            
            lote_dict = {
                "id": str(lote.id),
                "data_abate": lote.data_abate,
                "quantidade_aves": lote.quantidade_aves,
                "peso_total_kg": lote.peso_total_kg,
                "unidade": lote.unidade,
                "tipo_ave": lote.tipo_ave,
                "observacoes": lote.observacoes,
                "created_at": lote.created_at,
                "updated_at": lote.updated_at
            }
            
            # Testar se pode ser serializado para JSON
            try:
                json_str = json.dumps(lote_dict, default=str)
                print(f"  ✓ Serialização JSON OK")
                result.append(lote_dict)
            except Exception as e:
                print(f"  ✗ Erro na serialização JSON: {e}")
                
        print(f"\n✓ Processados {len(result)} lotes com sucesso")
        
    except Exception as e:
        print(f"✗ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_serialization())