import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def verificar_calculos_lucro():
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    db = client['abatedouro']
    
    # Buscar alguns abates para verificar os cálculos
    abates = await db.abates_completos.find(
        {}, 
        {
            'data_abate': 1, 
            'receita_bruta': 1, 
            'custos_totais': 1, 
            'lucro_total': 1, 
            'lucro_liquido': 1
        }
    ).limit(15).to_list(None)
    
    print('Verificando cálculos de lucro:')
    print('=' * 80)
    
    inconsistencias = 0
    
    for abate in abates:
        data = abate.get('data_abate', 'N/A')
        receita = abate.get('receita_bruta', 0)
        custos = abate.get('custos_totais', 0)
        lucro_db = abate.get('lucro_total', 0)
        lucro_calculado = receita - custos
        
        diferenca = abs(lucro_db - lucro_calculado)
        
        status = "✓ OK" if diferenca < 0.01 else "✗ ERRO"
        if diferenca >= 0.01:
            inconsistencias += 1
            
        print(f"Data: {data}")
        print(f"  Receita: R$ {receita:,.2f}")
        print(f"  Custos:  R$ {custos:,.2f}")
        print(f"  Lucro Calculado: R$ {lucro_calculado:,.2f}")
        print(f"  Lucro no DB:     R$ {lucro_db:,.2f}")
        print(f"  Status: {status}")
        if diferenca >= 0.01:
            print(f"  Diferença: R$ {diferenca:,.2f}")
        print('-' * 40)
    
    print(f"\nResumo: {inconsistencias} inconsistências encontradas em {len(abates)} registros")
    
    # Verificar se há valores negativos de lucro
    lucros_negativos = await db.abates_completos.count_documents({'lucro_total': {'$lt': 0}})
    print(f"Registros com lucro negativo: {lucros_negativos}")
    
    if lucros_negativos > 0:
        print("\nExemplos de lucros negativos:")
        negativos = await db.abates_completos.find(
            {'lucro_total': {'$lt': 0}}, 
            {'data_abate': 1, 'receita_bruta': 1, 'custos_totais': 1, 'lucro_total': 1}
        ).limit(5).to_list(None)
        
        for neg in negativos:
            print(f"  {neg.get('data_abate')}: Receita R$ {neg.get('receita_bruta', 0):,.2f}, Custos R$ {neg.get('custos_totais', 0):,.2f}, Lucro R$ {neg.get('lucro_total', 0):,.2f}")

if __name__ == "__main__":
    asyncio.run(verificar_calculos_lucro())