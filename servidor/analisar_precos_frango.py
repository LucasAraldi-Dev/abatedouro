#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para analisar preços do kg do frango vivo na base de dados
"""

import pymongo
from datetime import datetime
import statistics
from collections import defaultdict
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configuração do MongoDB LOCAL
MONGODB_URI = 'mongodb://localhost:27017/'
MONGODB_DBNAME = 'abatedouro'

def main():
    """Função principal"""
    try:
        # Conectar ao MongoDB
        client = pymongo.MongoClient(MONGODB_URI)
        db = client[MONGODB_DBNAME]
        collection = db['abates_completos']
        
        print(f"Conectado ao banco: {MONGODB_DBNAME}")
        print("Analisando preços do kg do frango vivo...\n")
        
        # Buscar todos os abates
        abates = list(collection.find({}).sort('data_abate', 1))
        print(f"Encontrados {len(abates)} registros de abates")
        
        if not abates:
            print("Nenhum registro encontrado!")
            return
        
        # Análise geral dos preços
        precos = [abate.get('valor_kg_vivo', 0) for abate in abates if abate.get('valor_kg_vivo', 0) > 0]
        
        if precos:
            print("\n📊 ANÁLISE GERAL DOS PREÇOS:")
            print(f"Menor preço: R$ {min(precos):.2f}")
            print(f"Maior preço: R$ {max(precos):.2f}")
            print(f"Preço médio: R$ {statistics.mean(precos):.2f}")
            print(f"Mediana: R$ {statistics.median(precos):.2f}")
            if len(precos) > 1:
                print(f"Desvio padrão: R$ {statistics.stdev(precos):.2f}")
        
        # Análise por mês
        precos_por_mes = defaultdict(list)
        
        for abate in abates:
            data_abate = abate.get('data_abate')
            valor_kg = abate.get('valor_kg_vivo', 0)
            
            if isinstance(data_abate, datetime) and valor_kg > 0:
                mes_ano = data_abate.strftime('%Y-%m')
                precos_por_mes[mes_ano].append(valor_kg)
        
        print("\n📅 ANÁLISE POR MÊS:")
        for mes_ano in sorted(precos_por_mes.keys()):
            precos_mes = precos_por_mes[mes_ano]
            if precos_mes:
                print(f"\n{mes_ano}:")
                print(f"  Registros: {len(precos_mes)}")
                print(f"  Menor: R$ {min(precos_mes):.2f}")
                print(f"  Maior: R$ {max(precos_mes):.2f}")
                print(f"  Média: R$ {statistics.mean(precos_mes):.2f}")
                print(f"  Mediana: R$ {statistics.median(precos_mes):.2f}")
        
        # Verificar consistência dos cálculos
        print("\n🔍 VERIFICAÇÃO DE CONSISTÊNCIA:")
        inconsistencias = 0
        
        for i, abate in enumerate(abates[:10]):  # Verificar primeiros 10
            data_abate = abate.get('data_abate')
            if isinstance(data_abate, datetime):
                data_str = data_abate.strftime('%d/%m/%Y')
            else:
                data_str = str(data_abate)
            
            peso_total = abate.get('peso_total_kg', 0)
            valor_kg = abate.get('valor_kg_vivo', 0)
            valor_total_calculado = peso_total * valor_kg
            valor_total_registrado = abate.get('valor_total', 0)
            
            diferenca = abs(valor_total_calculado - valor_total_registrado)
            
            print(f"\nData: {data_str}")
            print(f"  Peso Total: {peso_total:.2f} kg")
            print(f"  Valor/kg: R$ {valor_kg:.2f}")
            print(f"  Valor Total Calculado: R$ {valor_total_calculado:.2f}")
            print(f"  Valor Total Registrado: R$ {valor_total_registrado:.2f}")
            print(f"  Diferença: R$ {diferenca:.2f}")
            
            if diferenca > 1.0:  # Diferença maior que R$ 1,00
                inconsistencias += 1
                print(f"  ⚠️ INCONSISTÊNCIA DETECTADA!")
            else:
                print(f"  ✅ Valores consistentes")
        
        if inconsistencias > 0:
            print(f"\n⚠️ {inconsistencias} inconsistências encontradas nos primeiros 10 registros")
        else:
            print(f"\n✅ Todos os valores verificados estão consistentes")
        
        # Comparação com valores de mercado esperados
        print("\n💰 COMPARAÇÃO COM VALORES DE MERCADO:")
        print("Valores típicos de mercado para frango vivo:")
        print("- Mínimo esperado: R$ 4,50 - R$ 5,50")
        print("- Médio esperado: R$ 5,50 - R$ 6,50")
        print("- Máximo esperado: R$ 6,50 - R$ 7,50")
        
        if precos:
            preco_medio_atual = statistics.mean(precos)
            if preco_medio_atual < 4.5:
                print(f"\n⚠️ Preço médio atual (R$ {preco_medio_atual:.2f}) está ABAIXO do esperado")
            elif preco_medio_atual > 7.5:
                print(f"\n⚠️ Preço médio atual (R$ {preco_medio_atual:.2f}) está ACIMA do esperado")
            else:
                print(f"\n✅ Preço médio atual (R$ {preco_medio_atual:.2f}) está dentro do esperado")
        
        # Verificar dados específicos de janeiro e fevereiro
        print("\n🔍 DADOS ESPECÍFICOS DE JANEIRO E FEVEREIRO 2025:")
        jan_fev_abates = list(collection.find({
            'data_abate': {
                '$gte': datetime(2025, 1, 1),
                '$lt': datetime(2025, 3, 1)
            }
        }).sort('data_abate', 1).limit(20))
        
        if jan_fev_abates:
            for abate in jan_fev_abates:
                data_abate = abate.get('data_abate')
                if isinstance(data_abate, datetime):
                    data_str = data_abate.strftime('%d/%m/%Y')
                else:
                    data_str = str(data_abate)
                
                valor_kg = abate.get('valor_kg_vivo', 0)
                peso_total = abate.get('peso_total_kg', 0)
                valor_total = abate.get('valor_total', 0)
                lucro_liquido = abate.get('lucro_liquido', 0)
                
                print(f"\n{data_str}:")
                print(f"  Valor/kg: R$ {valor_kg:.2f}")
                print(f"  Peso: {peso_total:.2f} kg")
                print(f"  Valor Total: R$ {valor_total:.2f}")
                print(f"  Lucro: R$ {lucro_liquido:.2f}")
        else:
            print("Nenhum dado encontrado para janeiro/fevereiro 2025")
        
        client.close()
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()