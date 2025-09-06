from typing import Dict, Any, Optional
from datetime import datetime

class MetricsCalculator:
    """Serviço para calcular métricas dos abates completos"""
    
    @staticmethod
    def calcular_metricas_completas(dados_abate: Dict[str, Any]) -> Dict[str, Any]:
        """Calcula todas as métricas derivadas do abate"""
        
        # Cálculos básicos dos produtos
        produtos = dados_abate.get('produtos', [])
        peso_total_produtos = sum(p.get('peso_kg', 0) for p in produtos)
        receita_produtos = sum(p.get('valor_total', 0) for p in produtos)
        
        # Cálculo das despesas fixas totais
        despesas = dados_abate.get('despesas_fixas', {})
        custos_fixos = sum([
            despesas.get('funcionarios', 0),
            despesas.get('agua', 0),
            despesas.get('energia', 0),
            despesas.get('embalagem', 0),
            despesas.get('refeicao', 0),
            despesas.get('materiais_limpeza', 0),
            despesas.get('gelo', 0),
            despesas.get('horas_extras', 0),
            despesas.get('amonia', 0),
            despesas.get('epi', 0),
            despesas.get('manutencao', 0),
            despesas.get('lenha_caldeira', 0),
            despesas.get('diaristas', 0),
            despesas.get('depreciacao', 0),
            despesas.get('recisao', 0),
            despesas.get('ferias', 0),
            despesas.get('inss', 0)
        ])
        
        # Cálculo do custo do frango vivo
        quantidade_aves = dados_abate.get('quantidade_aves', 0)
        valor_kg_vivo = dados_abate.get('valor_kg_vivo', 0)
        peso_medio_ave = dados_abate.get('peso_medio_ave', 0)
        peso_total_kg = dados_abate.get('peso_total_kg', 0)
        
        custo_frango_vivo = peso_total_kg * valor_kg_vivo
        custos_totais = custos_fixos + custo_frango_vivo
        
        # Métricas principais
        preco_venda_kg = receita_produtos / peso_total_produtos if peso_total_produtos > 0 else 0
        receita_bruta = receita_produtos
        lucro_liquido = receita_bruta - custos_totais
        rendimento_final = min((peso_total_produtos / peso_total_kg) * 100, 100.0) if peso_total_kg > 0 else 0
        
        # Cálculo de perdas
        peso_total_perdas = max(peso_total_kg - peso_total_produtos, 0)
        percentual_perda_total = (peso_total_perdas / peso_total_kg) * 100 if peso_total_kg > 0 else 0
        valor_perdas = peso_total_perdas * preco_venda_kg if preco_venda_kg > 0 else 0
        eficiencia_aproveitamento = min(rendimento_final, 100.0)
        
        # Indicadores por unidade
        media_valor_kg = receita_bruta / peso_total_produtos if peso_total_produtos > 0 else 0
        custo_kg = custos_totais / peso_total_produtos if peso_total_produtos > 0 else 0
        custo_abate_kg = custos_fixos / peso_total_produtos if peso_total_produtos > 0 else 0
        lucro_kg = lucro_liquido / peso_total_produtos if peso_total_produtos > 0 else 0
        # Novo: custo total por ave (inclui custos fixos + frango vivo)
        custo_ave = custos_totais / quantidade_aves if quantidade_aves > 0 else 0
        custo_franco_ajuste = custo_frango_vivo / quantidade_aves if quantidade_aves > 0 else 0
        custo_frango = custo_franco_ajuste
        lucro_frango = lucro_liquido / quantidade_aves if quantidade_aves > 0 else 0
        lucro_total = lucro_liquido
        
        # Indicadores de eficiência operacional
        horarios = dados_abate.get('horarios', {})
        horas_trabalhadas = horarios.get('horas_trabalhadas', 0)
        
        aves_hora = quantidade_aves / horas_trabalhadas if horas_trabalhadas > 0 else 0
        kg_hora = peso_total_produtos / horas_trabalhadas if horas_trabalhadas > 0 else 0
        tempo_medio_ave = (horas_trabalhadas * 60) / quantidade_aves if quantidade_aves > 0 else 0  # em minutos
        
        # Eficiência operacional baseada em múltiplos fatores
        eficiencia_base = 100
        if rendimento_final < 70:
            eficiencia_base -= (70 - rendimento_final) * 0.5
        if aves_hora < 50:
            eficiencia_base -= (50 - aves_hora) * 0.3
        if percentual_perda_total > 10:
            eficiencia_base -= (percentual_perda_total - 10) * 2
        
        eficiencia_operacional = max(min(eficiencia_base, 100.0), 0.0)
        
        # Indicadores de qualidade
        diversificacao_produtos = len(produtos)
        # Peso médio geral processado por ave (usando total de produtos)
        peso_medio_geral = (peso_total_produtos / quantidade_aves) if quantidade_aves > 0 else 0
        
        # Performance Score (0-100)
        score_performance = (
            (rendimento_final * 0.3) +
            (eficiencia_operacional * 0.3) +
            (min(aves_hora / 100 * 100, 100) * 0.2) +
            (min((100 - percentual_perda_total), 100) * 0.2)
        )
        
        # Classificação de performance
        if score_performance >= 90:
            classificacao_performance = "Excelente"
        elif score_performance >= 80:
            classificacao_performance = "Muito Bom"
        elif score_performance >= 70:
            classificacao_performance = "Bom"
        elif score_performance >= 60:
            classificacao_performance = "Regular"
        else:
            classificacao_performance = "Ruim"
        
        # Cálculos Cortes vs Inteiro
        cortes_peso_total = 0
        cortes_valor_total = 0
        inteiro_peso_total = 0
        inteiro_valor_total = 0
        
        for produto in produtos:
            tipo = produto.get('tipo', '').lower()
            peso = produto.get('peso_kg', 0)
            valor = produto.get('valor_total', 0)
            
            if 'inteiro' in tipo or 'inteira' in tipo:
                inteiro_peso_total += peso
                inteiro_valor_total += valor
            else:
                # Considera todos os outros como cortes
                cortes_peso_total += peso
                cortes_valor_total += valor
        
        # Percentuais Cortes vs Inteiro
        cortes_percentual_peso = (cortes_peso_total / peso_total_produtos) * 100 if peso_total_produtos > 0 else 0
        cortes_percentual_valor = (cortes_valor_total / receita_produtos) * 100 if receita_produtos > 0 else 0
        inteiro_percentual_peso = (inteiro_peso_total / peso_total_produtos) * 100 if peso_total_produtos > 0 else 0
        inteiro_percentual_valor = (inteiro_valor_total / receita_produtos) * 100 if receita_produtos > 0 else 0
        
        # Percentuais (garantidos entre 0 e 100 quando aplicável)
        def clamp(v: float, lo: float = 0.0, hi: float = 100.0) -> float:
            return max(lo, min(hi, v))
        
        # Notas:
        # - Alguns percentuais são referências base para exibição e podem ser 100 por definição
        # - Outros são calculados em relação a preço de venda/kg ou composição de custos
        percentual_receita_bruta = 100.0
        percentual_custos_totais = 100.0
        percentual_lucro_liquido = (lucro_liquido / receita_bruta) * 100 if receita_bruta > 0 else 0
        percentual_rendimento = rendimento_final
        percentual_media_valor_kg = 100.0
        percentual_custo_kg = 100.0
        percentual_custo_ave = 100.0
        percentual_custo_abate_kg = (custo_abate_kg / custo_kg) * 100 if custo_kg > 0 else 0
        percentual_custo_frango = (custo_frango / custo_ave) * 100 if custo_ave > 0 else 0
        percentual_lucro_kg = (lucro_kg / preco_venda_kg) * 100 if preco_venda_kg > 0 else 0
        # Receita por ave (para base do lucro_frango)
        receita_por_ave = (receita_bruta / quantidade_aves) if quantidade_aves > 0 else 0
        percentual_lucro_frango = (lucro_frango / receita_por_ave) * 100 if receita_por_ave > 0 else 0
        percentual_lucro_total = (lucro_liquido / receita_bruta) * 100 if receita_bruta > 0 else 0
        
        # Aplicar clamp onde faz sentido (evitar >100 ou <0 indevidos)
        percentual_receita_bruta = clamp(percentual_receita_bruta)
        percentual_custos_totais = clamp(percentual_custos_totais)
        percentual_lucro_liquido = clamp(percentual_lucro_liquido, -100.0, 100.0)
        percentual_rendimento = clamp(percentual_rendimento)
        percentual_media_valor_kg = clamp(percentual_media_valor_kg)
        percentual_custo_kg = clamp(percentual_custo_kg)
        percentual_custo_ave = clamp(percentual_custo_ave)
        percentual_custo_abate_kg = clamp(percentual_custo_abate_kg)
        percentual_custo_frango = clamp(percentual_custo_frango)
        percentual_lucro_kg = clamp(percentual_lucro_kg, -100.0, 100.0)
        percentual_lucro_frango = clamp(percentual_lucro_frango, -100.0, 100.0)
        percentual_lucro_total = clamp(percentual_lucro_total, -100.0, 100.0)
        
        # Retornar todas as métricas calculadas
        metricas = {
            # Métricas principais
            'peso_inteiro_abatido': round(peso_total_produtos, 2),
            'preco_venda_kg': round(preco_venda_kg, 2),
            'receita_bruta': round(receita_bruta, 2),
            'custos_totais': round(custos_totais, 2),
            'lucro_liquido': round(lucro_liquido, 2),
            'rendimento_final': round(rendimento_final, 2),
            
            # Métricas Cortes vs Inteiro
            'cortes_peso_total': round(cortes_peso_total, 2),
            'cortes_valor_total': round(cortes_valor_total, 2),
            'cortes_percentual_peso': round(cortes_percentual_peso, 2),
            'cortes_percentual_valor': round(cortes_percentual_valor, 2),
            'inteiro_peso_total': round(inteiro_peso_total, 2),
            'inteiro_valor_total': round(inteiro_valor_total, 2),
            'inteiro_percentual_peso': round(inteiro_percentual_peso, 2),
            'inteiro_percentual_valor': round(inteiro_percentual_valor, 2),
            
            # Indicadores por unidade
            'media_valor_kg': round(media_valor_kg, 2),
            'custo_kg': round(custo_kg, 2),
            'custo_ave': round(custo_ave, 2),
            'custo_abate_kg': round(custo_abate_kg, 2),
            'custo_frango': round(custo_frango, 2),
            'lucro_kg': round(lucro_kg, 2),
            'lucro_frango': round(lucro_frango, 2),
            'lucro_total': round(lucro_total, 2),
            
            # Indicadores de eficiência operacional
            'aves_hora': round(aves_hora, 2),
            'kg_hora': round(kg_hora, 2),
            'tempo_medio_ave': round(tempo_medio_ave, 2),
            'eficiencia_operacional': round(eficiencia_operacional, 2),
            
            # Análise de perdas
            'peso_total_perdas': round(peso_total_perdas, 2),
            'percentual_perda_total': round(percentual_perda_total, 2),
            'valor_perdas': round(valor_perdas, 2),
            'eficiencia_aproveitamento': round(eficiencia_aproveitamento, 2),
            
            # Indicadores de qualidade
            'diversificacao_produtos': diversificacao_produtos,
            'peso_medio_geral': round(peso_medio_geral, 2),
            
            # Performance Score
            'score_performance': round(score_performance, 2),
            'classificacao_performance': classificacao_performance,
            
            # Percentuais
            'percentual_receita_bruta': round(percentual_receita_bruta, 2),
            'percentual_custos_totais': round(percentual_custos_totais, 2),
            'percentual_lucro_liquido': round(percentual_lucro_liquido, 2),
            'percentual_rendimento': round(percentual_rendimento, 2),
            'percentual_media_valor_kg': round(percentual_media_valor_kg, 2),
            'percentual_custo_kg': round(percentual_custo_kg, 2),
            'percentual_custo_ave': round(percentual_custo_ave, 2),
            'percentual_custo_abate_kg': round(percentual_custo_abate_kg, 2),
            'percentual_custo_frango': round(percentual_custo_frango, 2),
            'percentual_lucro_kg': round(percentual_lucro_kg, 2),
            'percentual_lucro_frango': round(percentual_lucro_frango, 2),
            'percentual_lucro_total': round(percentual_lucro_total, 2)
        }
        
        return metricas