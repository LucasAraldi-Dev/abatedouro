import asyncio
import sys
import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

# Adicionar o diretório do projeto ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.metrics_calculator import MetricsCalculator

async def fix_missing_metrics():
    """Corrige métricas faltantes em todos os registros do banco"""
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    db = client['abatedouro']
    collection = db['abates_completos']
    
    print("Iniciando correção de métricas faltantes...")
    
    # Buscar registros com métricas nulas
    query = {
        "$or": [
            {"lucro_liquido": None},
            {"rendimento_final": None},
            {"eficiencia_operacional": None},
            {"receita_bruta": None},
            {"custos_totais": None}
        ]
    }
    
    docs_to_fix = await collection.find(query).to_list(length=None)
    total_docs = len(docs_to_fix)
    
    print(f"Encontrados {total_docs} registros com métricas faltantes")
    
    if total_docs == 0:
        print("Nenhum registro precisa ser corrigido.")
        client.close()
        return
    
    calculator = MetricsCalculator()
    updated_count = 0
    error_count = 0
    
    for i, doc in enumerate(docs_to_fix, 1):
        try:
            print(f"Processando registro {i}/{total_docs} - Data: {doc.get('data_abate')}")
            
            # Calcular métricas
            metricas = calculator.calcular_metricas_completas(doc)
            
            # Atualizar o documento
            metricas['updated_at'] = datetime.utcnow()
            
            result = await collection.update_one(
                {"_id": doc["_id"]},
                {"$set": metricas}
            )
            
            if result.modified_count > 0:
                updated_count += 1
                print(f"  ✓ Atualizado com sucesso")
            else:
                print(f"  ⚠ Nenhuma modificação necessária")
                
        except Exception as e:
            error_count += 1
            print(f"  ✗ Erro ao processar: {str(e)}")
    
    print(f"\n" + "="*60)
    print(f"Correção concluída!")
    print(f"Registros processados: {total_docs}")
    print(f"Registros atualizados: {updated_count}")
    print(f"Erros encontrados: {error_count}")
    
    # Verificar resultado final
    remaining_null = await collection.count_documents(query)
    print(f"Registros ainda com métricas nulas: {remaining_null}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(fix_missing_metrics())