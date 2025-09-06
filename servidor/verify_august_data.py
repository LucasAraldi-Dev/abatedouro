#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar os dados de abate inseridos para agosto de 2025
"""

import pymongo
from datetime import datetime
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configuração do MongoDB LOCAL
MONGODB_URI = 'mongodb://localhost:27017/'
MONGODB_DBNAME = 'abatedouro'

def main():
    """Função principal de verificação"""
    try:
        # Conectar ao MongoDB
        client = pymongo.MongoClient(MONGODB_URI)
        db = client[MONGODB_DBNAME]
        collection = db['abates_completos']
        
        print(f"Conectado ao banco: {MONGODB_DBNAME}")
        print("Verificando dados de agosto de 2025...\n")
        
        # Buscar dados de agosto
        inicio_agosto = datetime(2025, 8, 1)
        fim_agosto = datetime(2025, 8, 31, 23, 59, 59)
        
        abates_agosto = list(collection.find({
            'data_abate': {
                '$gte': inicio_agosto,
                '$lte': fim_agosto
            }
        }).sort('data_abate', 1))
        
        print(f"📊 Encontrados {len(abates_agosto)} registros de abate em agosto/2025")
        
        if len(abates_agosto) == 0:
            print("❌ Nenhum dado encontrado para agosto!")
            return False
        
        # Estatísticas gerais
        total_aves = sum(a['quantidade_aves'] for a in abates_agosto)
        total_receita = sum(a['receita_bruta'] for a in abates_agosto)
        total_lucro = sum(a['lucro_liquido'] for a in abates_agosto)
        media_aves = total_aves / len(abates_agosto)
        media_receita = total_receita / len(abates_agosto)
        
        print(f"\n📈 Estatísticas do mês:")
        print(f"Total de aves abatidas: {total_aves:,}")
        print(f"Receita bruta total: R$ {total_receita:,.2f}")
        print(f"Lucro líquido total: R$ {total_lucro:,.2f}")
        print(f"Média de aves por dia: {media_aves:,.0f}")
        print(f"Média de receita por dia: R$ {media_receita:,.2f}")
        
        # Verificar alguns dias específicos
        print(f"\n🔍 Detalhes de alguns dias:")
        for i, abate in enumerate(abates_agosto[:5]):  # Primeiros 5 dias
            data_str = abate['data_abate'].strftime('%d/%m/%Y')
            print(f"  {data_str}: {abate['quantidade_aves']:,} aves, R$ {abate['receita_bruta']:,.2f}, {abate['classificacao_performance']}")
        
        if len(abates_agosto) > 5:
            print(f"  ... e mais {len(abates_agosto) - 5} dias")
        
        # Verificar estrutura de um registro
        primeiro_abate = abates_agosto[0]
        print(f"\n🔧 Verificação de estrutura (primeiro registro):")
        print(f"  ID: {primeiro_abate['_id']}")
        print(f"  Data: {primeiro_abate['data_abate']}")
        print(f"  Quantidade de produtos: {len(primeiro_abate['produtos'])}")
        print(f"  Horários: {primeiro_abate['horarios']['hora_inicio']} às {primeiro_abate['horarios']['hora_termino']}")
        print(f"  Rendimento: {primeiro_abate['rendimento_final']:.2f}%")
        print(f"  Score performance: {primeiro_abate['score_performance']:.1f}")
        
        # Verificar range de datas
        datas_encontradas = [a['data_abate'].day for a in abates_agosto]
        datas_esperadas = list(range(1, 32))  # 1 a 31
        datas_faltando = set(datas_esperadas) - set(datas_encontradas)
        
        if datas_faltando:
            print(f"\n⚠️  Dias faltando: {sorted(datas_faltando)}")
        else:
            print(f"\n✅ Todos os 31 dias de agosto estão presentes!")
        
        # Verificar produtos
        produtos_unicos = set()
        for abate in abates_agosto:
            for produto in abate['produtos']:
                produtos_unicos.add(produto['nome'])
        
        print(f"\n🥩 Produtos encontrados ({len(produtos_unicos)}):")
        for produto in sorted(produtos_unicos):
            print(f"  - {produto}")
        
        # Verificar performance
        performances = [a['classificacao_performance'] for a in abates_agosto]
        from collections import Counter
        contador_performance = Counter(performances)
        
        print(f"\n📊 Distribuição de performance:")
        for perf, count in contador_performance.items():
            print(f"  {perf}: {count} dias ({count/len(abates_agosto)*100:.1f}%)")
        
        client.close()
        print(f"\n✅ Verificação concluída com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro na verificação: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()