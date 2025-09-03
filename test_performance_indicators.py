#!/usr/bin/env python3
"""
Script de teste para verificar se todos os indicadores de performance
estão sendo salvos corretamente no banco de dados.
"""

import requests
import json
from datetime import datetime, date
from decimal import Decimal

# Configuração da API
BASE_URL = "http://localhost:8000/api/v1"

def test_performance_indicators_save():
    """
    Testa o salvamento completo de um abate com todos os indicadores de performance.
    """
    
    # Dados de teste para um abate completo
    abate_data = {
        # Dados básicos obrigatórios
        "data_abate": "2024-01-15T08:00:00",
        "quantidade_aves": 1000,
        "valor_kg_vivo": 5.50,
        "peso_total_kg": 2500.0,
        "peso_medio_ave": 2.5,
        "valor_total": 13750.0,
        "unidade": "Unidade Principal",
        "tipo_ave": "frango",
        "observacoes": "Teste de salvamento de indicadores",
        
        # Horários obrigatórios
        "horarios": {
            "hora_inicio": "08:00",
            "hora_termino": "16:00",
            "intervalo_minutos": 60,
            "horas_trabalhadas": 7.0,
            "horas_reais": 8.0
        },
        
        # Produtos com estrutura correta
        "produtos": [
            {
                "nome": "Frango Inteiro",
                "tipo": "Carcaça",
                "peso_kg": 1000.0,
                "preco_kg": 12.50,
                "valor_total": 12500.0,
                "percentual": 50.0
            },
            {
                "nome": "Coxa e Sobrecoxa",
                "tipo": "Corte",
                "peso_kg": 600.0,
                "preco_kg": 15.00,
                "valor_total": 9000.0,
                "percentual": 30.0
            }
        ],
        
        # Despesas fixas com estrutura correta
        "despesas_fixas": {
            "funcionarios": 500.0,
            "agua": 150.0,
            "energia": 200.0,
            "embalagem": 100.0,
            "refeicao": 80.0,
            "materiais_limpeza": 50.0,
            "gelo": 30.0,
            "horas_extras": 100.0,
            "amonia": 25.0,
            "epi": 40.0,
            "manutencao": 75.0,
            "lenha_caldeira": 60.0,
            "diaristas": 120.0,
            "depreciacao": 200.0,
            "recisao": 50.0,
            "ferias": 80.0,
            "inss": 150.0,
            "frango_morto_plataforma": 30.0,
            "escaldagem_eviceracao": 40.0,
            "pe_graxaria": 20.0,
            "descarte": 15.0
        },
        
        # Dados financeiros adicionais
        "peso_inteiro_abatido": 2000.0,
        "preco_venda_kg": 12.50,
        
        # Indicadores de performance (calculados)
        "receita_bruta": 10750.0,
        "custos_totais": 5850.0,
        "lucro_liquido": 4900.0,
        "rendimento_final": 83.7,
        "media_valor_kg": 5.38,
        "custo_kg": 2.93,
        "custo_ave": 5.85,
        "custo_abate_kg": 0.43,
        "custo_frango": 5.00,
        "lucro_kg": 2.45,
        "lucro_frango": 4.90,
        "lucro_total": 4900.0,
        
        # Percentuais
        "percentual_receita_bruta": 100.0,
        "percentual_custos_totais": 54.4,
        "percentual_lucro_liquido": 45.6,
        "percentual_rendimento": 80.0,
        "percentual_media_valor_kg": 100.0,
        "percentual_custo_kg": 54.4,
        "percentual_custo_ave": 54.4,
        "percentual_custo_abate_kg": 8.0,
        "percentual_custo_frango": 46.5,
        "percentual_lucro_kg": 45.6,
        "percentual_lucro_frango": 45.6,
        "percentual_lucro_total": 45.6,
        
        # Eficiência operacional
        "aves_hora": 125.0,
        "kg_hora": 250.0,
        "tempo_medio_ave": 0.48,
        "eficiencia_operacional": 87.5,
        
        # Análise de perdas
        "peso_total_perdas": 500.0,
        "percentual_perda_total": 20.0,
        "valor_perdas": 1250.0,
        "eficiencia_aproveitamento": 80.0,
        
        # Indicadores de qualidade
        "diversificacao_produtos": 2,
        "peso_medio_geral": 2.5,
        
        # Pontuação de performance
        "score_performance": 8.5,
        "classificacao_performance": "Excelente"
    }
    
    print("=== TESTE DE SALVAMENTO DE INDICADORES DE PERFORMANCE ===")
    print(f"Enviando dados para: {BASE_URL}/abates-completos/")
    
    try:
        # Enviar dados para a API
        response = requests.post(
            f"{BASE_URL}/abates-completos/",
            json=abate_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status da resposta: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            abate_id = result.get("id")
            print(f"✅ Abate criado com sucesso! ID: {abate_id}")
            
            # Verificar se os dados foram salvos corretamente
            print("\n=== VERIFICANDO DADOS SALVOS ===")
            verify_response = requests.get(f"{BASE_URL}/abates-completos/{abate_id}")
            
            if verify_response.status_code == 200:
                saved_data = verify_response.json()
                
                # Lista de indicadores para verificar
                indicators_to_check = [
                    "receita_bruta", "custos_totais", "lucro_liquido", "rendimento_final",
                    "media_valor_kg", "custo_kg", "custo_ave", "custo_abate_kg",
                    "custo_frango", "lucro_kg", "lucro_frango", "lucro_total",
                    "aves_hora", "kg_hora", "tempo_medio_ave", "eficiencia_operacional",
                    "peso_total_perdas", "percentual_perda_total", "valor_perdas",
                    "eficiencia_aproveitamento", "diversificacao_produtos", "peso_medio_geral",
                    "score_performance", "classificacao_performance"
                ]
                
                print("\n📊 INDICADORES SALVOS:")
                missing_indicators = []
                
                for indicator in indicators_to_check:
                    if indicator in saved_data and saved_data[indicator] is not None:
                        value = saved_data[indicator]
                        print(f"  ✅ {indicator}: {value}")
                    else:
                        missing_indicators.append(indicator)
                        print(f"  ❌ {indicator}: AUSENTE")
                
                # Verificar percentuais
                percentage_indicators = [
                    "percentual_receita_bruta", "percentual_custos_totais", "percentual_lucro_liquido",
                    "percentual_rendimento", "percentual_media_valor_kg", "percentual_custo_kg",
                    "percentual_custo_ave", "percentual_custo_abate_kg", "percentual_custo_frango",
                    "percentual_lucro_kg", "percentual_lucro_frango", "percentual_lucro_total"
                ]
                
                print("\n📈 PERCENTUAIS SALVOS:")
                for indicator in percentage_indicators:
                    if indicator in saved_data and saved_data[indicator] is not None:
                        value = saved_data[indicator]
                        print(f"  ✅ {indicator}: {value}%")
                    else:
                        missing_indicators.append(indicator)
                        print(f"  ❌ {indicator}: AUSENTE")
                
                # Resumo final
                print("\n=== RESUMO DO TESTE ===")
                total_indicators = len(indicators_to_check) + len(percentage_indicators)
                saved_indicators = total_indicators - len(missing_indicators)
                
                print(f"Total de indicadores testados: {total_indicators}")
                print(f"Indicadores salvos corretamente: {saved_indicators}")
                print(f"Indicadores ausentes: {len(missing_indicators)}")
                
                if missing_indicators:
                    print(f"\n❌ INDICADORES AUSENTES: {', '.join(missing_indicators)}")
                    return False
                else:
                    print("\n🎉 TODOS OS INDICADORES FORAM SALVOS CORRETAMENTE!")
                    return True
                    
            else:
                print(f"❌ Erro ao verificar dados salvos: {verify_response.status_code}")
                print(verify_response.text)
                return False
                
        else:
            print(f"❌ Erro ao criar abate: {response.status_code}")
            print(response.text)
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Erro de conexão. Verifique se o servidor está rodando em http://localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_performance_indicators_save()
    if success:
        print("\n✅ TESTE CONCLUÍDO COM SUCESSO!")
    else:
        print("\n❌ TESTE FALHOU - Verifique os logs acima para mais detalhes.")