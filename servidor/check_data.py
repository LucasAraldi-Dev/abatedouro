import os
import sys
sys.path.append('.')

from app.db import get_db
from app.crud.abate_completo import crud_abate_completo
from app.crud.lote_abate import crud_lote_abate
from app.crud.produto import crud_produto

def main():
    try:
        print("Conectando ao banco de dados...")
        db = get_db()
        print("✓ Conexão estabelecida")
        
        # Verificar abates completos
        abates_count = crud_abate_completo.count(db)
        print(f"Total de abates completos: {abates_count}")
        
        if abates_count > 0:
            # Pegar alguns exemplos
            abates = crud_abate_completo.get_multi(db, limit=3)
            print("\nExemplos de abates completos:")
            for i, abate in enumerate(abates, 1):
                print(f"  {i}. ID: {abate.id}")
                print(f"     Data: {abate.data_abate}")
                print(f"     Lucro Líquido: {getattr(abate, 'lucro_liquido', 'N/A')}")
                print(f"     Rendimento Final: {getattr(abate, 'rendimento_final', 'N/A')}")
                print(f"     Eficiência Operacional: {getattr(abate, 'eficiencia_operacional', 'N/A')}")
                print(f"     Score Performance: {getattr(abate, 'score_performance', 'N/A')}")
                print()
        
        # Verificar lotes
        lotes_count = crud_lote_abate.count(db)
        print(f"Total de lotes: {lotes_count}")
        
        # Verificar produtos
        produtos_count = crud_produto.count(db)
        print(f"Total de produtos: {produtos_count}")
        
    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
