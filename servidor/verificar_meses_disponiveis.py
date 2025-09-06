import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import json
from collections import defaultdict

async def verificar_meses_disponiveis():
    # Conectar ao MongoDB
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    db = client['abatedouro']
    collection = db['abates_completos']
    
    print("=== VERIFICANDO MESES DISPONÍVEIS ===")
    print()
    
    try:
        # Buscar todos os registros
        total_docs = await collection.count_documents({})
        print(f"📊 Total de documentos na coleção: {total_docs}")
        
        if total_docs == 0:
            print("❌ Nenhum documento encontrado")
            return
        
        # Buscar alguns registros para análise
        registros = await collection.find().limit(10).to_list(None)
        
        print("\n📋 Analisando primeiros registros:")
        print("-" * 80)
        
        meses_encontrados = defaultdict(list)
        
        for i, registro in enumerate(registros):
            data_abate = registro.get('data_abate')
            peso_total = registro.get('peso_total_kg', 0)
            custos_totais = registro.get('custos_totais', 0)
            receita_bruta = registro.get('receita_bruta', 0)
            valor_kg_vivo = registro.get('valor_kg_vivo', 0)
            preco_venda_kg = registro.get('preco_venda_kg', 0)
            
            print(f"\nRegistro {i+1}:")
            print(f"  Data: {data_abate} (tipo: {type(data_abate)})")
            print(f"  Peso total: {peso_total:.2f} kg")
            print(f"  Custos totais: R$ {custos_totais:.2f}")
            print(f"  Receita bruta: R$ {receita_bruta:.2f}")
            print(f"  valor_kg_vivo: R$ {valor_kg_vivo:.2f}")
            print(f"  preco_venda_kg: R$ {preco_venda_kg:.2f}")
            
            # Calcular preços como no gráfico
            if peso_total > 0:
                preco_vivo_calc = custos_totais / peso_total
                preco_abatido_calc = receita_bruta / peso_total
                print(f"  Preço vivo calculado: R$ {preco_vivo_calc:.2f}")
                print(f"  Preço abatido calculado: R$ {preco_abatido_calc:.2f}")
                
                if preco_vivo_calc < 1.0:
                    print(f"  ⚠️  PROBLEMA: Preço vivo muito baixo!")
            
            # Extrair mês/ano da data
            if data_abate:
                try:
                    if isinstance(data_abate, str):
                        data_obj = datetime.fromisoformat(data_abate.replace('Z', '+00:00'))
                    else:
                        data_obj = data_abate
                    
                    mes_ano = f"{data_obj.year}-{data_obj.month:02d}"
                    meses_encontrados[mes_ano].append(registro)
                except Exception as e:
                    print(f"  ❌ Erro ao processar data: {e}")
        
        print("\n📅 Meses encontrados:")
        print("-" * 50)
        
        nomes_meses = [
            'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
            'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
        ]
        
        for mes_ano in sorted(meses_encontrados.keys()):
            ano, mes = mes_ano.split('-')
            nome_mes = f"{nomes_meses[int(mes)-1]} {ano}"
            registros_mes = meses_encontrados[mes_ano]
            
            # Calcular totais do mês
            total_peso = sum(r.get('peso_total_kg', 0) for r in registros_mes)
            total_custos = sum(r.get('custos_totais', 0) for r in registros_mes)
            total_receita = sum(r.get('receita_bruta', 0) for r in registros_mes)
            
            preco_vivo = total_custos / total_peso if total_peso > 0 else 0
            preco_abatido = total_receita / total_peso if total_peso > 0 else 0
            
            print(f"{nome_mes}: {len(registros_mes)} registros")
            print(f"  Preço vivo: R$ {preco_vivo:.2f}")
            print(f"  Preço abatido: R$ {preco_abatido:.2f}")
            
            if preco_vivo < 1.0:
                print(f"  ⚠️  PROBLEMA: Preço vivo suspeito!")
        
        # Buscar mais registros se necessário
        if total_docs > 10:
            print(f"\n... e mais {total_docs - 10} registros na base")
            
            # Fazer uma consulta agregada simples
            print("\n🔍 Fazendo análise geral dos dados...")
            
            pipeline = [
                {
                    '$group': {
                        '_id': None,
                        'total_registros': {'$sum': 1},
                        'peso_total': {'$sum': '$peso_total_kg'},
                        'custos_total': {'$sum': '$custos_totais'},
                        'receita_total': {'$sum': '$receita_bruta'},
                        'min_data': {'$min': '$data_abate'},
                        'max_data': {'$max': '$data_abate'}
                    }
                }
            ]
            
            resultado_geral = await collection.aggregate(pipeline).to_list(None)
            
            if resultado_geral:
                dados = resultado_geral[0]
                peso_total = dados['peso_total']
                custos_total = dados['custos_total']
                receita_total = dados['receita_total']
                
                preco_vivo_geral = custos_total / peso_total if peso_total > 0 else 0
                preco_abatido_geral = receita_total / peso_total if peso_total > 0 else 0
                
                print(f"\n📊 RESUMO GERAL:")
                print(f"Total de registros: {dados['total_registros']}")
                print(f"Período: {dados['min_data']} a {dados['max_data']}")
                print(f"Peso total: {peso_total:,.2f} kg")
                print(f"Custos totais: R$ {custos_total:,.2f}")
                print(f"Receita total: R$ {receita_total:,.2f}")
                print(f"Preço médio frango vivo: R$ {preco_vivo_geral:.2f}")
                print(f"Preço médio frango abatido: R$ {preco_abatido_geral:.2f}")
                
                if preco_vivo_geral < 1.0:
                    print(f"\n⚠️  PROBLEMA IDENTIFICADO:")
                    print(f"   O preço médio do frango vivo ({preco_vivo_geral:.2f}) está muito baixo!")
                    print(f"   Isso indica que há problema nos dados de custos_totais.")
    
    except Exception as e:
        print(f"❌ Erro geral: {e}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(verificar_meses_disponiveis())