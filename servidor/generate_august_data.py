#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para gerar dados de abate do período de 01-08 a 31-08 de 2025
Baseado na estrutura do abate do dia 01-09
"""

import pymongo
import random
from datetime import datetime, timedelta
from bson import ObjectId
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configuração do MongoDB LOCAL
MONGODB_URI = 'mongodb://localhost:27017/'
MONGODB_DBNAME = 'abatedouro'

# Produtos base com IDs reais
PRODUTOS_BASE = [
    {"produto_id": "68b0e56353c3275b6f2fb04a", "nome": "PEITO", "tipo": "Peito", "preco_base": 14.5, "peso_base": 988},
    {"produto_id": "68b0e5ac53c3275b6f2fb04b", "nome": "COXA C SOBRE", "tipo": "Coxa", "preco_base": 10.5, "peso_base": 5032},
    {"produto_id": "68b0e5c153c3275b6f2fb04c", "nome": "ASA", "tipo": "Asa", "preco_base": 16, "peso_base": 1630},
    {"produto_id": "68b0e5cf53c3275b6f2fb04d", "nome": "FILÉ DE PEITO", "tipo": "Peito", "preco_base": 19.99, "peso_base": 3012},
    {"produto_id": "68b0e60153c3275b6f2fb04e", "nome": "SASSAMI", "tipo": "Peito", "preco_base": 19.8, "peso_base": 612},
    {"produto_id": "68b0e9d753c3275b6f2fb051", "nome": "PERTENCE", "tipo": "Miúdos", "preco_base": 2.49, "peso_base": 4368},
    {"produto_id": "68b0e9e753c3275b6f2fb052", "nome": "MOELA", "tipo": "Miúdos", "preco_base": 9.5, "peso_base": 264},
    {"produto_id": "68b0e9f153c3275b6f2fb053", "nome": "CORAÇÃO", "tipo": "Miúdos", "preco_base": 30, "peso_base": 176},
    {"produto_id": "68b45578dc20de695c3522b9", "nome": "FIGADO", "tipo": "Miúdos", "preco_base": 8, "peso_base": 648},
    {"produto_id": "68b0ea2053c3275b6f2fb056", "nome": "CABEÇA", "tipo": "Outros", "preco_base": 1.99, "peso_base": 120},
    {"produto_id": "68b0ea2f53c3275b6f2fb057", "nome": "PÉS", "tipo": "Miúdos", "preco_base": 4.5, "peso_base": 195},
    {"produto_id": "68b0ee9a53c3275b6f2fb059", "nome": "PASSARINHA", "tipo": "Outros", "preco_base": 9.49, "peso_base": 600},
    {"produto_id": "68b0eea653c3275b6f2fb05a", "nome": "PESCOÇO", "tipo": "Miúdos", "preco_base": 3.99, "peso_base": 280},
    {"produto_id": "68b0eebd53c3275b6f2fb05c", "nome": "SOBRECOXA", "tipo": "Sobrecoxa", "preco_base": 10.49, "peso_base": 12},
    {"produto_id": "68b0ef6953c3275b6f2fb05d", "nome": "FRANGO INTEIRO", "tipo": "Congelado", "preco_base": 10, "peso_base": 3060},
    {"produto_id": "68b0ef7253c3275b6f2fb05e", "nome": "FRANGO INTEIRO ", "tipo": "Resfriado", "preco_base": 10.3, "peso_base": 1000},
    {"produto_id": "68b0efad53c3275b6f2fb061", "nome": "CARCAÇA 0,9", "tipo": "Carcaça", "preco_base": 13, "peso_base": 594},
    {"produto_id": "68b0efbc53c3275b6f2fb062", "nome": "CARCAÇA 1,0", "tipo": "Carcaça", "preco_base": 13, "peso_base": 1188},
    {"produto_id": "68b0efc853c3275b6f2fb063", "nome": "CARCAÇA 1,1", "tipo": "Carcaça", "preco_base": 13, "peso_base": 1664},
    {"produto_id": "68b0efd253c3275b6f2fb064", "nome": "CARCAÇA 1,2", "tipo": "Carcaça", "preco_base": 13.3, "peso_base": 1363},
    {"produto_id": "68b0efe053c3275b6f2fb065", "nome": "CARCAÇA 1,3", "tipo": "Carcaça", "preco_base": 13.3, "peso_base": 858},
    {"produto_id": "68b0efed53c3275b6f2fb066", "nome": "CARCAÇA 1,4", "tipo": "Carcaça", "preco_base": 13, "peso_base": 431},
    {"produto_id": "68b0eff953c3275b6f2fb067", "nome": "CARCAÇA 1,5", "tipo": "Carcaça", "preco_base": 13, "peso_base": 156},
    {"produto_id": "68b0f00153c3275b6f2fb068", "nome": "CARCAÇA 1,6", "tipo": "Carcaça", "preco_base": 12.9, "peso_base": 57},
    {"produto_id": "68b0f01153c3275b6f2fb069", "nome": "CARCAÇA 1,7", "tipo": "Carcaça", "preco_base": 12.9, "peso_base": 18}
]

def gerar_variacao(valor_base, variacao_percentual=0.15):
    """Gera uma variação aleatória do valor base"""
    variacao = random.uniform(-variacao_percentual, variacao_percentual)
    return valor_base * (1 + variacao)

def calcular_metricas(dados_abate):
    """Calcula todas as métricas derivadas do abate"""
    # Cálculos básicos
    peso_total_produtos = sum(p['peso_kg'] for p in dados_abate['produtos'])
    receita_produtos = sum(p['valor_total'] for p in dados_abate['produtos'])
    
    # Despesas fixas totais
    despesas = dados_abate['despesas_fixas']
    custos_fixos = sum([
        despesas['funcionarios'], despesas['agua'], despesas['energia'],
        despesas['embalagem'], despesas['refeicao'], despesas['materiais_limpeza'],
        despesas['gelo'], despesas['horas_extras'], despesas['amonia'],
        despesas['epi'], despesas['manutencao'], despesas['lenha_caldeira'],
        despesas['diaristas'], despesas['depreciacao'], despesas['recisao'],
        despesas['ferias'], despesas['inss']
    ])
    
    # Cálculo do custo do frango vivo
    custo_frango_vivo = dados_abate['quantidade_aves'] * dados_abate['valor_kg_vivo'] * dados_abate['peso_medio_ave']
    custos_totais = custos_fixos + custo_frango_vivo
    
    # Métricas calculadas
    peso_inteiro_abatido = peso_total_produtos
    preco_venda_kg = receita_produtos / peso_inteiro_abatido if peso_inteiro_abatido > 0 else 0
    receita_bruta = receita_produtos
    lucro_liquido = receita_bruta - custos_totais
    rendimento_final = min((peso_inteiro_abatido / dados_abate['peso_total_kg']) * 100, 100.0) if dados_abate['peso_total_kg'] > 0 else 0
    
    # Perdas - garantir que sejam >= 0
    peso_total_perdas = max(dados_abate['peso_total_kg'] - peso_inteiro_abatido, 0)
    percentual_perda_total = max((peso_total_perdas / dados_abate['peso_total_kg']) * 100, 0.0) if dados_abate['peso_total_kg'] > 0 else 0
    valor_perdas = max(peso_total_perdas * dados_abate['valor_kg_vivo'], 0.0)
    
    # Custos por kg e ave
    custo_kg = custos_totais / peso_inteiro_abatido if peso_inteiro_abatido > 0 else 0
    custo_ave = custos_totais / dados_abate['quantidade_aves'] if dados_abate['quantidade_aves'] > 0 else 0
    custo_abate_kg = custos_fixos / peso_inteiro_abatido if peso_inteiro_abatido > 0 else 0
    custo_frango = custo_frango_vivo / dados_abate['quantidade_aves'] if dados_abate['quantidade_aves'] > 0 else 0
    
    # Lucros
    lucro_kg = preco_venda_kg - custo_kg
    lucro_frango = (receita_bruta / dados_abate['quantidade_aves']) - custo_ave if dados_abate['quantidade_aves'] > 0 else 0
    
    # Eficiência
    horas_reais = dados_abate['horarios']['horas_reais']
    aves_hora = dados_abate['quantidade_aves'] / horas_reais if horas_reais > 0 else 0
    kg_hora = peso_inteiro_abatido / horas_reais if horas_reais > 0 else 0
    tempo_medio_ave = horas_reais / dados_abate['quantidade_aves'] if dados_abate['quantidade_aves'] > 0 else 0
    
    # Eficiência operacional (baseada em aves/hora)
    eficiencia_operacional = min(100, (aves_hora / 2000) * 100)  # 2000 aves/hora como referência
    
    # Diversificação de produtos (número de produtos diferentes)
    tipos_produtos = len(set(p['tipo'] for p in dados_abate['produtos']))
    diversificacao_produtos = min(100, (tipos_produtos / 10) * 100)  # 10 tipos como máximo
    
    # Score de performance
    score_performance = (rendimento_final + eficiencia_operacional + diversificacao_produtos) / 3
    
    # Classificação
    if score_performance >= 80:
        classificacao = "Excelente"
    elif score_performance >= 70:
        classificacao = "Bom"
    elif score_performance >= 60:
        classificacao = "Regular"
    else:
        classificacao = "Ruim"
    
    # Atualizar dados calculados
    dados_abate.update({
        'peso_inteiro_abatido': peso_inteiro_abatido,
        'preco_venda_kg': preco_venda_kg,
        'receita_bruta': receita_bruta,
        'custos_totais': custos_totais,
        'lucro_liquido': lucro_liquido,
        'rendimento_final': rendimento_final,
        'media_valor_kg': preco_venda_kg,
        'custo_kg': custo_kg,
        'custo_ave': custo_ave,
        'custo_abate_kg': custo_abate_kg,
        'custo_frango': custo_frango,
        'lucro_kg': lucro_kg,
        'lucro_frango': lucro_frango,
        'lucro_total': lucro_liquido,
        'aves_hora': aves_hora,
        'kg_hora': kg_hora,
        'tempo_medio_ave': tempo_medio_ave,
        'eficiencia_operacional': eficiencia_operacional,
        'peso_total_perdas': peso_total_perdas,
        'percentual_perda_total': percentual_perda_total,
        'valor_perdas': valor_perdas,
        'eficiencia_aproveitamento': rendimento_final,
        'diversificacao_produtos': diversificacao_produtos,
        'peso_medio_geral': peso_inteiro_abatido / dados_abate['quantidade_aves'] if dados_abate['quantidade_aves'] > 0 else 0,
        'score_performance': score_performance,
        'classificacao_performance': classificacao,
        # Percentuais (todos em 100 para base)
        'percentual_receita_bruta': 100,
        'percentual_custos_totais': 100,
        'percentual_lucro_liquido': (lucro_liquido / receita_bruta) * 100 if receita_bruta > 0 else 0,
        'percentual_media_valor_kg': 100,
        'percentual_custo_kg': 100,
        'percentual_custo_ave': 100,
        'percentual_custo_abate_kg': (custo_abate_kg / custo_kg) * 100 if custo_kg > 0 else 0,
        'percentual_custo_frango': (custo_frango / custo_ave) * 100 if custo_ave > 0 else 0,
        'percentual_lucro_kg': (lucro_kg / preco_venda_kg) * 100 if preco_venda_kg > 0 else 0,
        'percentual_lucro_frango': (lucro_frango / (receita_bruta / dados_abate['quantidade_aves'])) * 100 if dados_abate['quantidade_aves'] > 0 else 0,
        'percentual_lucro_total': (lucro_liquido / receita_bruta) * 100 if receita_bruta > 0 else 0,
        'percentual_rendimento': rendimento_final
    })
    
    return dados_abate

def gerar_abate_dia(data):
    """Gera dados de abate para um dia específico"""
    # Variações base
    quantidade_aves = int(gerar_variacao(17392, 0.25))  # ±25%
    valor_kg_vivo = round(gerar_variacao(6, 0.10), 2)  # ±10%
    peso_medio_ave = round(gerar_variacao(2.096, 0.15), 3)  # ±15%
    peso_total_kg = int(quantidade_aves * peso_medio_ave)
    valor_total = int(peso_total_kg * valor_kg_vivo)
    
    # Horários variados
    hora_inicio = random.choice(["05:30", "06:00", "06:30"])
    hora_termino = random.choice(["17:30", "18:00", "18:30"])
    horas_trabalhadas = 12 + random.uniform(-1, 1)
    intervalo_minutos = random.randint(60, 120)
    horas_reais = horas_trabalhadas - (intervalo_minutos / 60)
    
    # Produtos com variações
    produtos = []
    for produto in PRODUTOS_BASE:
        peso_variado = int(gerar_variacao(produto['peso_base'], 0.30))
        preco_variado = round(gerar_variacao(produto['preco_base'], 0.08), 2)
        valor_total_produto = round(peso_variado * preco_variado, 2)
        
        produtos.append({
            "produto_id": produto['produto_id'],
            "nome": produto['nome'],
            "tipo": produto['tipo'],
            "peso_kg": peso_variado,
            "preco_kg": preco_variado,
            "valor_total": valor_total_produto,
            "percentual": 0
        })
    
    # Despesas fixas com pequenas variações
    despesas_fixas = {
        "funcionarios": int(gerar_variacao(8000, 0.05)),
        "agua": int(gerar_variacao(2000, 0.20)),
        "energia": int(gerar_variacao(6000, 0.15)),
        "embalagem": int(gerar_variacao(3000, 0.10)),
        "refeicao": int(gerar_variacao(450, 0.10)),
        "materiais_limpeza": int(gerar_variacao(150, 0.20)),
        "gelo": random.randint(0, 500),
        "horas_extras": int(gerar_variacao(600, 0.30)),
        "amonia": random.randint(0, 300),
        "epi": random.randint(0, 200),
        "manutencao": int(gerar_variacao(1000, 0.40)),
        "lenha_caldeira": int(gerar_variacao(800, 0.25)),
        "diaristas": int(gerar_variacao(980, 0.15)),
        "depreciacao": 1000,  # Fixo
        "recisao": int(gerar_variacao(750, 0.20)),
        "ferias": round(gerar_variacao(888.5, 0.10), 1),
        "inss": int(gerar_variacao(1600, 0.05)),
        "frango_morto_plataforma": random.randint(0, 100),
        "escaldagem_eviceracao": random.randint(0, 50),
        "pe_graxaria": random.randint(0, 30),
        "descarte": random.randint(0, 80)
    }
    
    # Estrutura base do abate
    abate = {
        "_id": ObjectId(),
        "data_abate": data,
        "quantidade_aves": quantidade_aves,
        "valor_kg_vivo": valor_kg_vivo,
        "peso_total_kg": peso_total_kg,
        "peso_medio_ave": peso_medio_ave,
        "valor_total": valor_total,
        "unidade": "Belo Jardim",
        "tipo_ave": "Frango de Corte",
        "observacoes": "",
        "horarios": {
            "hora_inicio": hora_inicio,
            "hora_termino": hora_termino,
            "intervalo_minutos": intervalo_minutos,
            "horas_trabalhadas": round(horas_trabalhadas, 2),
            "horas_reais": round(horas_reais, 2)
        },
        "produtos": produtos,
        "despesas_fixas": despesas_fixas,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    # Calcular métricas
    abate = calcular_metricas(abate)
    
    return abate

def main():
    """Função principal"""
    try:
        # Conectar ao MongoDB
        client = pymongo.MongoClient(MONGODB_URI)
        db = client[MONGODB_DBNAME]
        collection = db['abates_completos']
        
        print(f"Conectado ao banco: {MONGODB_DBNAME}")
        print("Gerando dados de abate para agosto de 2025...")
        
        # Gerar dados para cada dia de agosto
        abates_gerados = []
        for dia in range(1, 32):  # 1 a 31 de agosto
            data_abate = datetime(2025, 8, dia, 11, 0, 0)  # 11:00 AM
            abate = gerar_abate_dia(data_abate)
            abates_gerados.append(abate)
            print(f"Gerado abate para {dia:02d}/08/2025 - {abate['quantidade_aves']} aves")
        
        # Inserir no banco
        resultado = collection.insert_many(abates_gerados)
        print(f"\n✅ {len(resultado.inserted_ids)} registros inseridos com sucesso!")
        
        # Estatísticas
        total_aves = sum(a['quantidade_aves'] for a in abates_gerados)
        total_receita = sum(a['receita_bruta'] for a in abates_gerados)
        media_aves = total_aves / len(abates_gerados)
        
        print(f"\n📊 Estatísticas do mês:")
        print(f"Total de aves abatidas: {total_aves:,}")
        print(f"Receita bruta total: R$ {total_receita:,.2f}")
        print(f"Média de aves por dia: {media_aves:,.0f}")
        
        client.close()
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()