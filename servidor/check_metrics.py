import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

async def check_metrics():
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    db = client['abatedouro']
    collection = db['abates_completos']
    
    print("Verificando métricas nos registros...")
    
    # Buscar alguns registros recentes
    docs = await collection.find({}).sort("data_abate", -1).limit(10).to_list(length=10)
    
    print(f"\nTotal de registros encontrados: {len(docs)}")
    print("\n" + "="*80)
    
    for i, doc in enumerate(docs, 1):
        data_abate = doc.get('data_abate')
        lucro_liquido = doc.get('lucro_liquido')
        rendimento_final = doc.get('rendimento_final')
        eficiencia_operacional = doc.get('eficiencia_operacional')
        receita_bruta = doc.get('receita_bruta')
        custos_totais = doc.get('custos_totais')
        
        print(f"Registro {i}:")
        print(f"  Data: {data_abate}")
        print(f"  Receita Bruta: {receita_bruta}")
        print(f"  Custos Totais: {custos_totais}")
        print(f"  Lucro Líquido: {lucro_liquido}")
        print(f"  Rendimento Final: {rendimento_final}%")
        print(f"  Eficiência Operacional: {eficiencia_operacional}%")
        print("-" * 50)
    
    # Verificar quantos registros têm métricas nulas
    null_lucro = await collection.count_documents({"lucro_liquido": None})
    null_rendimento = await collection.count_documents({"rendimento_final": None})
    null_eficiencia = await collection.count_documents({"eficiencia_operacional": None})
    
    total_docs = await collection.count_documents({})
    
    print(f"\nEstatísticas de métricas nulas:")
    print(f"Total de registros: {total_docs}")
    print(f"Registros com lucro_liquido = None: {null_lucro}")
    print(f"Registros com rendimento_final = None: {null_rendimento}")
    print(f"Registros com eficiencia_operacional = None: {null_eficiencia}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(check_metrics())