#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar preços do frango vivo vs valores de mercado
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
        
        print("🔍 ANÁLISE DE PREÇOS DO FRANGO VIVO\n")
        
        # Buscar todos os abates
        abates = list(collection.find({}).sort('data_abate', 1))
        print(f"Total de registros: {len(abates)}")
        
        # Análise geral dos preços
        precos = [abate.get('valor_kg_vivo', 0) for abate in abates if abate.get('valor_kg_vivo', 0) > 0]
        
        if precos:
            print(f"\n📊 RESUMO GERAL:")
            print(f"Menor preço: R$ {min(precos):.2f}")
            print(f"Maior preço: R$ {max(precos):.2f}")
            print(f"Preço médio: R$ {statistics.mean(precos):.2f}")
            print(f"Mediana: R$ {statistics.median(precos):.2f}")
        
        # Análise por mês com foco em jan/fev
        precos_por_mes = defaultdict(list)
        
        for abate in abates:
            data_abate = abate.get('data_abate')
            valor_kg = abate.get('valor_kg_vivo', 0)
            
            if isinstance(data_abate, datetime) and valor_kg > 0:
                mes_ano = data_abate.strftime('%Y-%m')
                precos_por_mes[mes_ano].append(valor_kg)
        
        print(f"\n📅 PREÇOS POR MÊS (foco jan/fev):")
        meses_interesse = ['2025-01', '2025-02', '2025-03']
        
        for mes_ano in meses_interesse:
            if mes_ano in precos_por_mes:
                precos_mes = precos_por_mes[mes_ano]
                print(f"\n{mes_ano}:")
                print(f"  Registros: {len(precos_mes)}")
                print(f"  Menor: R$ {min(precos_mes):.2f}")
                print(f"  Maior: R$ {max(precos_mes):.2f}")
                print(f"  Média: R$ {statistics.mean(precos_mes):.2f}")
        
        # Comparação com valores de mercado
        print(f"\n💰 COMPARAÇÃO COM VALORES DE MERCADO:")
        print(f"Valores típicos para frango vivo (2025):")
        print(f"- Faixa baixa: R$ 4,50 - R$ 5,50")
        print(f"- Faixa média: R$ 5,50 - R$ 6,50")
        print(f"- Faixa alta: R$ 6,50 - R$ 7,50")
        
        # Análise específica jan/fev
        if '2025-01' in precos_por_mes and '2025-02' in precos_por_mes:
            jan_precos = precos_por_mes['2025-01']
            fev_precos = precos_por_mes['2025-02']
            
            jan_media = statistics.mean(jan_precos)
            fev_media = statistics.mean(fev_precos)
            
            print(f"\n🎯 ANÁLISE JANEIRO/FEVEREIRO:")
            print(f"Janeiro 2025 - Média: R$ {jan_media:.2f}")
            print(f"Fevereiro 2025 - Média: R$ {fev_media:.2f}")
            
            # Verificar se estão dentro da faixa esperada
            if jan_media < 4.5:
                print(f"⚠️ Janeiro: Preço MUITO BAIXO (abaixo de R$ 4,50)")
            elif jan_media < 5.5:
                print(f"✅ Janeiro: Preço na faixa baixa (R$ 4,50 - R$ 5,50)")
            elif jan_media < 6.5:
                print(f"✅ Janeiro: Preço na faixa média (R$ 5,50 - R$ 6,50)")
            else:
                print(f"⚠️ Janeiro: Preço alto (acima de R$ 6,50)")
            
            if fev_media < 4.5:
                print(f"⚠️ Fevereiro: Preço MUITO BAIXO (abaixo de R$ 4,50)")
            elif fev_media < 5.5:
                print(f"✅ Fevereiro: Preço na faixa baixa (R$ 4,50 - R$ 5,50)")
            elif fev_media < 6.5:
                print(f"✅ Fevereiro: Preço na faixa média (R$ 5,50 - R$ 6,50)")
            else:
                print(f"⚠️ Fevereiro: Preço alto (acima de R$ 6,50)")
        
        # Verificar se há problema com o valor base usado na geração
        print(f"\n🔧 VERIFICAÇÃO DO VALOR BASE:")
        print(f"No script generate_jan_jul_data.py, o valor base é 6.35 com variação de ±0.08")
        print(f"Isso deveria gerar preços entre R$ 6,27 e R$ 6,43")
        
        if '2025-01' in precos_por_mes:
            jan_precos = precos_por_mes['2025-01']
            jan_min = min(jan_precos)
            jan_max = max(jan_precos)
            
            print(f"\nJaneiro real: R$ {jan_min:.2f} - R$ {jan_max:.2f}")
            
            if jan_min < 6.20 or jan_max > 6.50:
                print(f"⚠️ PROBLEMA: Os preços de janeiro estão fora da faixa esperada!")
                print(f"Esperado: R$ 6,27 - R$ 6,43")
                print(f"Real: R$ {jan_min:.2f} - R$ {jan_max:.2f}")
            else:
                print(f"✅ Preços de janeiro estão na faixa esperada")
        
        # Verificar alguns registros específicos
        print(f"\n🔍 AMOSTRA DE REGISTROS JANEIRO:")
        jan_abates = list(collection.find({
            'data_abate': {
                '$gte': datetime(2025, 1, 1),
                '$lt': datetime(2025, 2, 1)
            }
        }).sort('data_abate', 1).limit(5))
        
        for abate in jan_abates:
            data_abate = abate.get('data_abate')
            if isinstance(data_abate, datetime):
                data_str = data_abate.strftime('%d/%m/%Y')
            else:
                data_str = str(data_abate)
            
            valor_kg = abate.get('valor_kg_vivo', 0)
            print(f"{data_str}: R$ {valor_kg:.2f}")
        
        client.close()
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()