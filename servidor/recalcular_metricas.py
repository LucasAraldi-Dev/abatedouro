#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para recalcular métricas dos abates existentes com a correção do custo do frango vivo
"""

import pymongo
from datetime import datetime
from app.services.metrics_calculator import MetricsCalculator
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
        print("Recalculando métricas dos abates existentes...")
        
        # Buscar todos os abates
        abates = list(collection.find({}))
        print(f"Encontrados {len(abates)} abates para recalcular")
        
        contador_atualizados = 0
        
        for abate in abates:
            try:
                # Converter ObjectId para string se necessário
                abate_id = abate['_id']
                
                # Recalcular métricas
                metricas_novas = MetricsCalculator.calcular_metricas_completas(abate)
                
                # Atualizar no banco
                resultado = collection.update_one(
                    {'_id': abate_id},
                    {'$set': {
                        **metricas_novas,
                        'updated_at': datetime.utcnow()
                    }}
                )
                
                if resultado.modified_count > 0:
                    contador_atualizados += 1
                    data_abate = abate.get('data_abate', 'N/A')
                    if isinstance(data_abate, datetime):
                        data_str = data_abate.strftime('%d/%m/%Y')
                    else:
                        data_str = str(data_abate)
                    
                    print(f"Atualizado abate de {data_str} - Lucro: R$ {metricas_novas.get('lucro_liquido', 0):.2f}")
                    
            except Exception as e:
                print(f"Erro ao processar abate {abate.get('_id', 'N/A')}: {e}")
                continue
        
        print(f"\n✅ {contador_atualizados} abates atualizados com sucesso!")
        
        # Verificar alguns dados de janeiro e fevereiro
        print("\n📊 Verificando dados de janeiro e fevereiro:")
        jan_fev_abates = list(collection.find({
            'data_abate': {
                '$gte': datetime(2025, 1, 1),
                '$lt': datetime(2025, 3, 1)
            }
        }).limit(5))
        
        for abate in jan_fev_abates:
            data_abate = abate.get('data_abate')
            if isinstance(data_abate, datetime):
                data_str = data_abate.strftime('%d/%m/%Y')
            else:
                data_str = str(data_abate)
            
            lucro_liquido = abate.get('lucro_liquido', 0)
            lucro_kg = abate.get('lucro_kg', 0)
            lucro_frango = abate.get('lucro_frango', 0)
            
            print(f"Data: {data_str}")
            print(f"  Lucro Total: R$ {lucro_liquido:.2f}")
            print(f"  Lucro por Kg: R$ {lucro_kg:.2f}")
            print(f"  Lucro por Ave: R$ {lucro_frango:.2f}")
            print("---")
        
        client.close()
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()