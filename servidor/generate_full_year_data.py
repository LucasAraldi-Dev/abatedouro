import pymongo
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any
import calendar

# Configuração do MongoDB
MONGO_URL = "mongodb://localhost:27017/"
DATABASE_NAME = "abatedouro"
COLLECTION_NAME = "abates_completos"

# Dados base do arquivo abates.md
PRODUTOS_BASE = [
    {"produto_id": "68b0e56353c3275b6f2fb04a", "nome": "PEITO", "tipo": "Peito", "peso_base": 988, "preco_base": 14.5},
    {"produto_id": "68b0e5ac53c3275b6f2fb04b", "nome": "COXA C SOBRE", "tipo": "Coxa", "peso_base": 5032, "preco_base": 10.5},
    {"produto_id": "68b0e5c153c3275b6f2fb04c", "nome": "ASA", "tipo": "Asa", "peso_base": 1630, "preco_base": 16},
    {"produto_id": "68b0e5cf53c3275b6f2fb04d", "nome": "FILÉ DE PEITO", "tipo": "Peito", "peso_base": 3012, "preco_base": 19.99},
    {"produto_id": "68b0e60153c3275b6f2fb04e", "nome": "SASSAMI", "tipo": "Peito", "peso_base": 612, "preco_base": 19.8},
    {"produto_id": "68b0e9d753c3275b6f2fb051", "nome": "PERTENCE", "tipo": "Miúdos", "peso_base": 4368, "preco_base": 2.49},
    {"produto_id": "68b0e9e753c3275b6f2fb052", "nome": "MOELA", "tipo": "Miúdos", "peso_base": 264, "preco_base": 9.5},
    {"produto_id": "68b0e9f153c3275b6f2fb053", "nome": "CORAÇÃO", "tipo": "Miúdos", "peso_base": 176, "preco_base": 30},
    {"produto_id": "68b45578dc20de695c3522b9", "nome": "FIGADO", "tipo": "Miúdos", "peso_base": 648, "preco_base": 8},
    {"produto_id": "68b0ea2053c3275b6f2fb056", "nome": "CABEÇA", "tipo": "Outros", "peso_base": 120, "preco_base": 1.99},
    {"produto_id": "68b0ea2f53c3275b6f2fb057", "nome": "PÉS", "tipo": "Miúdos", "peso_base": 195, "preco_base": 4.5},
    {"produto_id": "68b0ee9a53c3275b6f2fb059", "nome": "PASSARINHA", "tipo": "Outros", "peso_base": 600, "preco_base": 9.49},
    {"produto_id": "68b0eea653c3275b6f2fb05a", "nome": "PESCOÇO", "tipo": "Miúdos", "peso_base": 280, "preco_base": 3.99},
    {"produto_id": "68b0eebd53c3275b6f2fb05c", "nome": "SOBRECOXA", "tipo": "Sobrecoxa", "peso_base": 12, "preco_base": 10.49},
    {"produto_id": "68b0ef6953c3275b6f2fb05d", "nome": "FRANGO INTEIRO", "tipo": "Congelado", "peso_base": 3060, "preco_base": 10},
    {"produto_id": "68b0ef7253c3275b6f2fb05e", "nome": "FRANGO INTEIRO ", "tipo": "Resfriado", "peso_base": 1000, "preco_base": 10.3},
    {"produto_id": "68b0efad53c3275b6f2fb061", "nome": "CARCAÇA 0,9", "tipo": "Carcaça", "peso_base": 594, "preco_base": 13},
    {"produto_id": "68b0efbc53c3275b6f2fb062", "nome": "CARCAÇA 1,0", "tipo": "Carcaça", "peso_base": 1188, "preco_base": 13},
    {"produto_id": "68b0efc853c3275b6f2fb063", "nome": "CARCAÇA 1,1", "tipo": "Carcaça", "peso_base": 1664, "preco_base": 13},
    {"produto_id": "68b0efd253c3275b6f2fb064", "nome": "CARCAÇA 1,2", "tipo": "Carcaça", "peso_base": 1363, "preco_base": 13.3},
    {"produto_id": "68b0efe053c3275b6f2fb065", "nome": "CARCAÇA 1,3", "tipo": "Carcaça", "peso_base": 858, "preco_base": 13.3},
    {"produto_id": "68b0efed53c3275b6f2fb066", "nome": "CARCAÇA 1,4", "tipo": "Carcaça", "peso_base": 431, "preco_base": 13},
    {"produto_id": "68b0eff953c3275b6f2fb067", "nome": "CARCAÇA 1,5", "tipo": "Carcaça", "peso_base": 156, "preco_base": 13},
    {"produto_id": "68b0f00153c3275b6f2fb068", "nome": "CARCAÇA 1,6", "tipo": "Carcaça", "peso_base": 57, "preco_base": 12.9},
    {"produto_id": "68b0f01153c3275b6f2fb069", "nome": "CARCAÇA 1,7", "tipo": "Carcaça", "peso_base": 18, "preco_base": 12.9}
]

# Despesas fixas base
DESPESAS_BASE = {
    "funcionarios": 8000,
    "agua": 2000,
    "energia": 6000,
    "embalagem": 3000,
    "refeicao": 450,
    "materiais_limpeza": 150,
    "gelo": 0,
    "horas_extras": 600,
    "amonia": 0,
    "epi": 0,
    "manutencao": 1000,
    "lenha_caldeira": 800,
    "diaristas": 980,
    "depreciacao": 1000,
    "recisao": 750,
    "ferias": 888.5,
    "inss": 1600,
    "frango_morto_plataforma": 0,
    "escaldagem_eviceracao": 0,
    "pe_graxaria": 0,
    "descarte": 0
}

def obter_fator_sazonal(mes: int) -> Dict[str, float]:
    """Retorna fatores sazonais para custos e preços baseado no mês"""
    # Inverno (Jun-Ago): custos mais altos, demanda maior
    # Verão (Dez-Fev): custos menores, demanda menor
    # Outono/Primavera: valores intermediários
    
    fatores_sazonais = {
        1: {"custo": 0.95, "preco": 0.98, "demanda": 0.90},  # Janeiro - verão
        2: {"custo": 0.92, "preco": 0.95, "demanda": 0.88},  # Fevereiro - verão
        3: {"custo": 0.98, "preco": 1.02, "demanda": 0.95},  # Março - outono
        4: {"custo": 1.02, "preco": 1.05, "demanda": 1.00},  # Abril - outono
        5: {"custo": 1.08, "preco": 1.10, "demanda": 1.05},  # Maio - outono/inverno
        6: {"custo": 1.15, "preco": 1.18, "demanda": 1.15},  # Junho - inverno
        7: {"custo": 1.20, "preco": 1.22, "demanda": 1.20},  # Julho - inverno
        8: {"custo": 1.18, "preco": 1.20, "demanda": 1.18},  # Agosto - inverno
        9: {"custo": 1.05, "preco": 1.08, "demanda": 1.02},  # Setembro - primavera
        10: {"custo": 1.00, "preco": 1.03, "demanda": 0.98}, # Outubro - primavera
        11: {"custo": 0.96, "preco": 0.99, "demanda": 0.92}, # Novembro - primavera/verão
        12: {"custo": 0.94, "preco": 0.97, "demanda": 0.90}  # Dezembro - verão
    }
    
    return fatores_sazonais.get(mes, {"custo": 1.0, "preco": 1.0, "demanda": 1.0})

def gerar_variacao_produtos(produtos_base: List[Dict], fator_sazonal: Dict[str, float]) -> List[Dict]:
    """Gera variações nos produtos baseado em fatores sazonais"""
    produtos = []
    
    for produto in produtos_base:
        # Variação no peso (±15%)
        variacao_peso = random.uniform(0.85, 1.15)
        peso_kg = round(produto["peso_base"] * variacao_peso * fator_sazonal["demanda"], 1)
        
        # Variação no preço (±10% + fator sazonal)
        variacao_preco = random.uniform(0.90, 1.10)
        preco_kg = round(produto["preco_base"] * variacao_preco * fator_sazonal["preco"], 2)
        
        valor_total = round(peso_kg * preco_kg, 2)
        
        produtos.append({
            "produto_id": produto["produto_id"],
            "nome": produto["nome"],
            "tipo": produto["tipo"],
            "peso_kg": peso_kg,
            "preco_kg": preco_kg,
            "valor_total": valor_total,
            "percentual": 0
        })
    
    return produtos

def gerar_variacao_despesas(despesas_base: Dict, fator_sazonal: Dict[str, float]) -> Dict:
    """Gera variações nas despesas baseado em fatores sazonais"""
    despesas = {}
    
    # Despesas que variam com a sazonalidade
    despesas_variaveis = ["energia", "agua", "lenha_caldeira", "gelo", "amonia"]
    
    for item, valor_base in despesas_base.items():
        if item in despesas_variaveis:
            # Variação maior para despesas sazonais
            variacao = random.uniform(0.80, 1.20)
            despesas[item] = round(valor_base * variacao * fator_sazonal["custo"], 2)
        else:
            # Variação menor para despesas fixas
            variacao = random.uniform(0.95, 1.05)
            despesas[item] = round(valor_base * variacao, 2)
    
    return despesas

def calcular_metricas(data: Dict) -> Dict:
    """Calcula todas as métricas baseado nos dados de entrada"""
    # Cálculos básicos
    peso_total_produtos = sum(p["peso_kg"] for p in data["produtos"])
    receita_bruta = sum(p["valor_total"] for p in data["produtos"])
    custos_totais = sum(data["despesas_fixas"].values())
    lucro_liquido = receita_bruta - custos_totais
    
    # Peso inteiro abatido (peso total + perdas estimadas)
    peso_inteiro_abatido = peso_total_produtos / random.uniform(0.75, 0.85)
    
    # Métricas de rendimento
    rendimento_final = min((peso_total_produtos / peso_inteiro_abatido) * 100, 100)
    peso_total_perdas = max(peso_inteiro_abatido - peso_total_produtos, 0)
    percentual_perda_total = (peso_total_perdas / peso_inteiro_abatido) * 100
    valor_perdas = max(peso_total_perdas * (receita_bruta / peso_total_produtos), 0)
    
    # Métricas de custo e lucro
    preco_venda_kg = receita_bruta / peso_total_produtos if peso_total_produtos > 0 else 0
    custo_kg = custos_totais / peso_total_produtos if peso_total_produtos > 0 else 0
    custo_ave = custos_totais / data["quantidade_aves"] if data["quantidade_aves"] > 0 else 0
    lucro_kg = preco_venda_kg - custo_kg
    lucro_frango = lucro_liquido / data["quantidade_aves"] if data["quantidade_aves"] > 0 else 0
    
    # Métricas de eficiência
    horas_reais = data["horarios"]["horas_reais"]
    aves_hora = data["quantidade_aves"] / horas_reais if horas_reais > 0 else 0
    kg_hora = peso_total_produtos / horas_reais if horas_reais > 0 else 0
    tempo_medio_ave = horas_reais / data["quantidade_aves"] if data["quantidade_aves"] > 0 else 0
    
    # Score de performance
    eficiencia_operacional = min(aves_hora / 20, 100)  # Base: 2000 aves/hora = 100%
    diversificacao_produtos = len([p for p in data["produtos"] if p["peso_kg"] > 0]) * 4  # Max 25 produtos
    peso_medio_geral = peso_total_produtos / data["quantidade_aves"] if data["quantidade_aves"] > 0 else 0
    
    score_performance = (rendimento_final + eficiencia_operacional + min(diversificacao_produtos, 100)) / 3
    
    # Classificação de performance
    if score_performance >= 85:
        classificacao = "Excelente"
    elif score_performance >= 70:
        classificacao = "Bom"
    elif score_performance >= 55:
        classificacao = "Regular"
    else:
        classificacao = "Ruim"
    
    # Percentuais (todos em 100 para compatibilidade)
    percentuais = {
        "percentual_receita_bruta": 100,
        "percentual_custos_totais": 100,
        "percentual_lucro_liquido": (lucro_liquido / receita_bruta) * 100 if receita_bruta > 0 else 0,
        "percentual_rendimento": rendimento_final,
        "percentual_media_valor_kg": 100,
        "percentual_custo_kg": 100,
        "percentual_custo_ave": 100,
        "percentual_custo_abate_kg": (custo_kg / preco_venda_kg) * 100 if preco_venda_kg > 0 else 0,
        "percentual_custo_frango": 100 - ((custo_kg / preco_venda_kg) * 100 if preco_venda_kg > 0 else 0),
        "percentual_lucro_kg": (lucro_kg / preco_venda_kg) * 100 if preco_venda_kg > 0 else 0,
        "percentual_lucro_frango": (lucro_kg / preco_venda_kg) * 100 if preco_venda_kg > 0 else 0,
        "percentual_lucro_total": (lucro_liquido / receita_bruta) * 100 if receita_bruta > 0 else 0
    }
    
    return {
        "peso_inteiro_abatido": round(peso_inteiro_abatido, 1),
        "preco_venda_kg": round(preco_venda_kg, 2),
        "receita_bruta": round(receita_bruta, 2),
        "custos_totais": round(custos_totais, 2),
        "lucro_liquido": round(lucro_liquido, 2),
        "rendimento_final": round(rendimento_final, 2),
        "media_valor_kg": round(preco_venda_kg, 2),
        "custo_kg": round(custo_kg, 2),
        "custo_ave": round(custo_ave, 2),
        "custo_abate_kg": round(custo_kg * 0.12, 2),  # Estimativa 12% do custo total
        "custo_frango": round(custo_ave * 0.88, 2),   # Restante do custo
        "lucro_kg": round(lucro_kg, 2),
        "lucro_frango": round(lucro_frango, 2),
        "lucro_total": round(lucro_liquido, 2),
        "aves_hora": round(aves_hora, 2),
        "kg_hora": round(kg_hora, 2),
        "tempo_medio_ave": round(tempo_medio_ave, 6),
        "eficiencia_operacional": round(eficiencia_operacional, 2),
        "peso_total_perdas": round(peso_total_perdas, 1),
        "percentual_perda_total": round(percentual_perda_total, 2),
        "valor_perdas": round(valor_perdas, 2),
        "eficiencia_aproveitamento": round(rendimento_final, 2),
        "diversificacao_produtos": round(diversificacao_produtos, 2),
        "peso_medio_geral": round(peso_medio_geral, 6),
        "score_performance": round(score_performance, 2),
        "classificacao_performance": classificacao,
        **percentuais
    }

def gerar_abate_dia(data_abate: datetime) -> Dict[str, Any]:
    """Gera dados de abate para um dia específico"""
    fator_sazonal = obter_fator_sazonal(data_abate.month)
    
    # Dados básicos com variação
    quantidade_aves = random.randint(12000, 22000)
    valor_kg_vivo = round(random.uniform(5.5, 6.5) * fator_sazonal["preco"], 2)
    peso_medio_ave = round(random.uniform(1.8, 2.3), 6)
    peso_total_kg = round(quantidade_aves * peso_medio_ave, 1)
    valor_total = round(peso_total_kg * valor_kg_vivo, 2)
    
    # Horários de trabalho
    hora_inicio = random.choice(["05:30", "06:00", "06:30"])
    horas_trabalhadas = random.randint(10, 14)
    intervalo_minutos = random.randint(60, 120)
    horas_reais = horas_trabalhadas - (intervalo_minutos / 60)
    
    if hora_inicio == "05:30":
        hora_termino_int = 5.5 + horas_trabalhadas
    elif hora_inicio == "06:00":
        hora_termino_int = 6 + horas_trabalhadas
    else:
        hora_termino_int = 6.5 + horas_trabalhadas
    
    hora_termino = f"{int(hora_termino_int):02d}:{int((hora_termino_int % 1) * 60):02d}"
    
    # Gerar produtos e despesas com variação sazonal
    produtos = gerar_variacao_produtos(PRODUTOS_BASE, fator_sazonal)
    despesas_fixas = gerar_variacao_despesas(DESPESAS_BASE, fator_sazonal)
    
    # Estrutura base do abate
    abate = {
        "data_abate": data_abate,
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
            "horas_trabalhadas": horas_trabalhadas,
            "horas_reais": round(horas_reais, 2)
        },
        "produtos": produtos,
        "despesas_fixas": despesas_fixas,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    
    # Calcular métricas
    metricas = calcular_metricas(abate)
    abate.update(metricas)
    
    return abate

def main():
    """Função principal para gerar dados de janeiro a agosto de 2025"""
    # Conectar ao MongoDB
    client = pymongo.MongoClient(MONGO_URL)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    
    print("🚀 Iniciando geração de dados de 01-01 a 31-08 de 2025...")
    
    # Gerar dados para cada dia do período
    dados_abates = []
    data_atual = datetime(2025, 1, 1)
    data_fim = datetime(2025, 8, 31)
    
    while data_atual <= data_fim:
        abate = gerar_abate_dia(data_atual)
        dados_abates.append(abate)
        print(f"Gerado abate para {data_atual.strftime('%d/%m/%Y')} - {abate['quantidade_aves']} aves")
        data_atual += timedelta(days=1)
    
    # Inserir no banco
    print(f"\nInserindo {len(dados_abates)} registros no banco...")
    result = collection.insert_many(dados_abates)
    print(f"✅ {len(result.inserted_ids)} registros inseridos com sucesso!")
    
    # Estatísticas do período
    total_aves = sum(abate["quantidade_aves"] for abate in dados_abates)
    receita_total = sum(abate["receita_bruta"] for abate in dados_abates)
    media_aves_dia = total_aves / len(dados_abates)
    
    print(f"\n📊 Estatísticas do período (Jan-Ago 2025):")
    print(f"Total de dias: {len(dados_abates)}")
    print(f"Total de aves abatidas: {total_aves:,}")
    print(f"Receita bruta total: R$ {receita_total:,.2f}")
    print(f"Média de aves por dia: {media_aves_dia:,.0f}")

if __name__ == "__main__":
    main()