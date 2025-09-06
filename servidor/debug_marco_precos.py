import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import json

async def debug_precos_marco():
    # Conectar ao MongoDB
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    db = client['abatedouro']
    collection = db['abates_completos']
    
    print("=== DEBUG: Preços de Março 2025 ===")
    print()
    
    # Buscar dados de março de 2025
    pipeline = [
        {
            '$match': {
                'data_abate': {
                    '$gte': '2025-03-01',
                    '$lt': '2025-04-01'
                }
            }
        },
        {
            '$sort': {'data_abate': 1}
        }
    ]
    
    abates_marco = await collection.aggregate(pipeline).to_list(None)
    
    if not abates_marco:
        print("❌ Nenhum dado encontrado para março de 2025")
        return
    
    print(f"📊 Total de registros em março: {len(abates_marco)}")
    print()
    
    # Analisar cada registro
    total_peso = 0
    total_custos = 0
    total_receita = 0
    valores_kg_vivo = []
    precos_venda_kg = []
    
    print("📋 Detalhes dos registros:")
    print("-" * 80)
    
    for i, abate in enumerate(abates_marco[:10]):  # Mostrar apenas os primeiros 10
        data = abate.get('data_abate', 'N/A')
        peso_total = abate.get('peso_total_kg', 0)
        custos_totais = abate.get('custos_totais', 0)
        receita_bruta = abate.get('receita_bruta', 0)
        valor_kg_vivo = abate.get('valor_kg_vivo', 0)
        preco_venda_kg = abate.get('preco_venda_kg', 0)
        
        # Calcular preço baseado em custos (como está sendo feito no gráfico)
        preco_calculado_custos = custos_totais / peso_total if peso_total > 0 else 0
        preco_calculado_receita = receita_bruta / peso_total if peso_total > 0 else 0
        
        print(f"Dia {i+1:2d} - {data}:")
        print(f"  Peso Total: {peso_total:8.2f} kg")
        print(f"  Custos Totais: R$ {custos_totais:8.2f}")
        print(f"  Receita Bruta: R$ {receita_bruta:8.2f}")
        print(f"  valor_kg_vivo (BD): R$ {valor_kg_vivo:6.2f}")
        print(f"  preco_venda_kg (BD): R$ {preco_venda_kg:6.2f}")
        print(f"  Preço calc. custos: R$ {preco_calculado_custos:6.2f}")
        print(f"  Preço calc. receita: R$ {preco_calculado_receita:6.2f}")
        print()
        
        total_peso += peso_total
        total_custos += custos_totais
        total_receita += receita_bruta
        valores_kg_vivo.append(valor_kg_vivo)
        precos_venda_kg.append(preco_venda_kg)
    
    if len(abates_marco) > 10:
        print(f"... e mais {len(abates_marco) - 10} registros")
        print()
    
    # Calcular médias do mês
    media_valor_kg_vivo = sum(valores_kg_vivo) / len(valores_kg_vivo) if valores_kg_vivo else 0
    media_preco_venda_kg = sum(precos_venda_kg) / len(precos_venda_kg) if precos_venda_kg else 0
    
    # Simular cálculo do gráfico (agrupamento por mês)
    preco_vivo_grafico = total_custos / total_peso if total_peso > 0 else 0
    preco_abatido_grafico = total_receita / total_peso if total_peso > 0 else 0
    
    print("📈 RESUMO DO MÊS DE MARÇO:")
    print("=" * 50)
    print(f"Total de registros: {len(abates_marco)}")
    print(f"Peso total acumulado: {total_peso:,.2f} kg")
    print(f"Custos totais acumulados: R$ {total_custos:,.2f}")
    print(f"Receita total acumulada: R$ {total_receita:,.2f}")
    print()
    print(f"Média valor_kg_vivo (BD): R$ {media_valor_kg_vivo:.2f}")
    print(f"Média preco_venda_kg (BD): R$ {media_preco_venda_kg:.2f}")
    print()
    print(f"🎯 VALORES QUE APARECEM NO GRÁFICO:")
    print(f"Preço Frango Vivo: R$ {preco_vivo_grafico:.2f}")
    print(f"Preço Frango Abatido: R$ {preco_abatido_grafico:.2f}")
    print()
    
    # Verificar se há problema nos dados
    if preco_vivo_grafico < 1.0:
        print("⚠️  PROBLEMA IDENTIFICADO:")
        print(f"   O preço do frango vivo calculado ({preco_vivo_grafico:.2f}) está muito baixo!")
        print("   Isso indica que os custos_totais podem estar incorretos.")
        print()
        
        # Verificar alguns registros específicos
        print("🔍 Verificando registros com custos baixos:")
        for abate in abates_marco:
            custos = abate.get('custos_totais', 0)
            peso = abate.get('peso_total_kg', 0)
            if peso > 0 and custos / peso < 1.0:
                print(f"   Data: {abate.get('data_abate')} - Custo/kg: R$ {custos/peso:.2f}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(debug_precos_marco())