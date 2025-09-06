import asyncio
import sys
import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

# Adicionar o diretório app ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from services.metrics_calculator import MetricsCalculator

async def recalculate_all_metrics():
    """Recalcula todas as métricas de todos os registros"""
    
    # Conectar ao MongoDB
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client["abatedouro"]
    collection = db["abates_completos"]
    
    print("Iniciando recálculo de todas as métricas...")
    
    # Buscar todos os registros
    cursor = collection.find({})
    registros = await cursor.to_list(length=None)
    
    total_registros = len(registros)
    print(f"Encontrados {total_registros} registros para recalcular")
    
    if total_registros == 0:
        print("Nenhum registro encontrado.")
        return
    
    registros_atualizados = 0
    erros = 0
    
    calculator = MetricsCalculator()
    
    for i, registro in enumerate(registros, 1):
        try:
            data_abate = registro.get('data_abate', 'N/A')
            print(f"Processando registro {i}/{total_registros} - Data: {data_abate}")
            
            # Calcular novas métricas
            novas_metricas = calculator.calcular_metricas_completas(registro)
            
            # Atualizar o registro
            resultado = await collection.update_one(
                {"_id": registro["_id"]},
                {"$set": {
                    **novas_metricas,
                    "updated_at": datetime.utcnow()
                }}
            )
            
            if resultado.modified_count > 0:
                registros_atualizados += 1
                print("  ✓ Atualizado com sucesso")
            else:
                print("  ⚠ Nenhuma alteração necessária")
                
        except Exception as e:
            erros += 1
            print(f"  ✗ Erro ao processar registro: {str(e)}")
    
    print("\n" + "="*60)
    print("Recálculo concluído!")
    print(f"Registros processados: {total_registros}")
    print(f"Registros atualizados: {registros_atualizados}")
    print(f"Erros encontrados: {erros}")
    
    # Fechar conexão
    client.close()

if __name__ == "__main__":
    asyncio.run(recalculate_all_metrics())