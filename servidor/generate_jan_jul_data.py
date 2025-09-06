#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para gerar dados de abate do período de 01-01 a 31-07 de 2025
Gera dados realistas com validações corretas para o Pydantic
"""

import pymongo
import random
from datetime import datetime, timedelta
from bson import ObjectId
import os
from dotenv import load_dotenv
import calendar

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
    """Calcula métricas derivadas dos dados de abate com validações corretas"""
    
    # Calcular totais dos produtos
    peso_total_produtos = sum(p['peso_kg'] for p in dados_abate['produtos'])
    receita_bruta = sum(p['valor_total'] for p in dados_abate['produtos'])
    
    # Calcular despesas totais
    despesas_totais = sum(dados_abate['despesas_fixas'].values())
    
    # Calcular lucro bruto
    lucro_bruto = receita_bruta - despesas_totais
    
    # Calcular rendimento final (peso produtos / peso vivo) - limitado a 100%
    rendimento_final = min((peso_total_produtos / dados_abate['peso_total_kg']) * 100, 100.0)
    
    # Calcular perdas - garantir que seja >= 0
    peso_total_perdas = max(dados_abate['peso_total_kg'] - peso_total_produtos, 0)
    percentual_perda_total = max((peso_total_perdas / dados_abate['peso_total_kg']) * 100, 0.0)
    
    # Valor das perdas (estimativa baseada no preço médio) - garantir que seja >= 0
    preco_medio_kg = dados_abate['valor_total'] / dados_abate['peso_total_kg']
    valor_perdas = max(peso_total_perdas * preco_medio_kg, 0.0)
    
    # Eficiência de aproveitamento - limitado a 100%
    eficiencia_aproveitamento = min(rendimento_final, 100.0)
    
    # Percentual de rendimento - limitado a 100%
    percentual_rendimento = min(rendimento_final, 100.0)
    
    # Margem de lucro
    margem_lucro = (lucro_bruto / receita_bruta) * 100 if receita_bruta > 0 else 0
    
    # Custo por ave
    custo_por_ave = despesas_totais / dados_abate['quantidade_aves']
    
    # Receita por ave
    receita_por_ave = receita_bruta / dados_abate['quantidade_aves']
    
    # Lucro por ave
    lucro_por_ave = lucro_bruto / dados_abate['quantidade_aves']
    
    # Produtividade (aves por hora)
    produtividade_aves_hora = dados_abate['quantidade_aves'] / dados_abate['horarios']['horas_trabalhadas']
    
    # Adicionar métricas aos dados
    dados_abate.update({
        'peso_total_produtos_kg': round(peso_total_produtos, 2),
        'receita_bruta': round(receita_bruta, 2),
        'despesas_totais': round(despesas_totais, 2),
        'lucro_bruto': round(lucro_bruto, 2),
        'rendimento_final': round(rendimento_final, 2),
        'peso_total_perdas': int(peso_total_perdas),
        'percentual_perda_total': round(percentual_perda_total, 2),
        'valor_perdas': round(valor_perdas, 2),
        'eficiencia_aproveitamento': round(eficiencia_aproveitamento, 2),
        'percentual_rendimento': round(percentual_rendimento, 2),
        'margem_lucro': round(margem_lucro, 2),
        'custo_por_ave': round(custo_por_ave, 2),
        'receita_por_ave': round(receita_por_ave, 2),
        'lucro_por_ave': round(lucro_por_ave, 2),
        'produtividade_aves_hora': round(produtividade_aves_hora, 2)
    })
    
    return dados_abate

def gerar_abate_dia(data):
    """Gera dados de abate para um dia específico"""
    
    # Variações sazonais por mês
    mes = data.month
    if mes in [12, 1, 2]:  # Verão - maior demanda
        fator_sazonal = 1.2
    elif mes in [6, 7, 8]:  # Inverno - menor demanda
        fator_sazonal = 0.9
    else:  # Outono/Primavera
        fator_sazonal = 1.0
    
    # Quantidade de aves (variação realista)
    quantidade_base = 18000 * fator_sazonal
    quantidade_aves = int(gerar_variacao(quantidade_base, 0.25))
    
    # Peso médio por ave (kg)
    peso_medio_ave = round(gerar_variacao(1.8, 0.10), 3)
    
    # Peso total (kg)
    peso_total_kg = int(quantidade_aves * peso_medio_ave)
    
    # Valor por kg vivo
    valor_kg_vivo = round(gerar_variacao(6.35, 0.08), 2)
    
    # Valor total
    valor_total = round(peso_total_kg * valor_kg_vivo, 2)
    
    # Horários de trabalho
    hora_inicio = "06:00"
    intervalo_minutos = random.randint(45, 75)
    horas_trabalhadas = round(gerar_variacao(10.5, 0.15), 2)
    horas_reais = horas_trabalhadas - (intervalo_minutos / 60)
    
    # Calcular hora de término
    inicio_dt = datetime.strptime(hora_inicio, "%H:%M")
    fim_dt = inicio_dt + timedelta(hours=horas_trabalhadas)
    hora_termino = fim_dt.strftime("%H:%M")
    
    # Gerar produtos com variações
    produtos = []
    for produto_base in PRODUTOS_BASE:
        # Nem todos os produtos são produzidos todos os dias
        if random.random() < 0.85:  # 85% de chance de produzir cada produto
            peso_kg = round(gerar_variacao(produto_base["peso_base"], 0.20), 2)
            preco_kg = round(gerar_variacao(produto_base["preco_base"], 0.12), 2)
            valor_total = round(peso_kg * preco_kg, 2)
            
            produtos.append({
                "produto_id": produto_base["produto_id"],
                "nome": produto_base["nome"],
                "tipo": produto_base["tipo"],
                "peso_kg": peso_kg,
                "preco_kg": preco_kg,
                "valor_total": valor_total,
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
        print("Gerando dados de abate para janeiro a julho de 2025...")
        
        # Gerar dados para cada dia de janeiro a julho
        abates_gerados = []
        total_dias = 0
        
        for mes in range(1, 8):  # Janeiro a julho (1 a 7)
            # Obter número de dias no mês
            dias_no_mes = calendar.monthrange(2025, mes)[1]
            
            for dia in range(1, dias_no_mes + 1):
                data_abate = datetime(2025, mes, dia, 11, 0, 0)  # 11:00 AM
                abate = gerar_abate_dia(data_abate)
                abates_gerados.append(abate)
                total_dias += 1
                
                print(f"Gerado abate para {dia:02d}/{mes:02d}/2025 - {abate['quantidade_aves']} aves")
        
        # Inserir no banco em lotes para melhor performance
        print(f"\nInserindo {len(abates_gerados)} registros no banco...")
        resultado = collection.insert_many(abates_gerados)
        print(f"✅ {len(resultado.inserted_ids)} registros inseridos com sucesso!")
        
        # Estatísticas
        total_aves = sum(a['quantidade_aves'] for a in abates_gerados)
        total_receita = sum(a['receita_bruta'] for a in abates_gerados)
        media_aves = total_aves / len(abates_gerados)
        
        print(f"\n📊 Estatísticas do período (Jan-Jul 2025):")
        print(f"Total de dias: {total_dias}")
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