import pymongo
from datetime import datetime

# Conectar ao MongoDB remoto
client = pymongo.MongoClient('mongodb://lucasaraldi:R6pXvaislUmmKm8A@ac-nqlllrv-shard-00-00.tvwmq9c.mongodb.net:27017,ac-nqlllrv-shard-00-01.tvwmq9c.mongodb.net:27017,ac-nqlllrv-shard-00-02.tvwmq9c.mongodb.net:27017/abatedouro?ssl=true&authSource=admin&retryWrites=true&w=majority')

db = client['abatedouro']

try:
    
    print("=== VERIFICAÇÃO DAS DESPESAS FIXAS ===")
    
    # Buscar abates completos
    abates = list(db.abates_completos.find({}, {
        '_id': 0, 
        'data_abate': 1, 
        'despesas_fixas': 1
    }))
    
    print(f"Abates Completos: {len(abates)}")
    print()
    
    total_despesas = {
        'funcionarios': 0,
        'agua': 0,
        'energia': 0,
        'embalagem': 0,
        'gelo': 0,
        'manutencao': 0,
        'horas_extras': 0,
        'diaristas': 0
    }
    
    for i, abate in enumerate(abates, 1):
        print(f"{i}. Data: {abate.get('data_abate')}")
        despesas = abate.get('despesas_fixas', {})
        
        print(f"   Despesas Fixas:")
        for campo, valor in despesas.items():
            print(f"     {campo}: R$ {valor:.2f}")
            if campo in total_despesas:
                total_despesas[campo] += valor
        print()
    
    print("=== TOTAIS ACUMULADOS ===")
    total_geral = 0
    for campo, valor in total_despesas.items():
        print(f"{campo.capitalize()}: R$ {valor:.2f}")
        total_geral += valor
    
    print(f"\nTOTAL GERAL: R$ {total_geral:.2f}")
    
    # Calcular totais de férias, INSS e rescisão
    total_ferias = 0
    total_inss = 0
    total_recisao = 0
    
    for abate in abates:
        despesas = abate.get('despesas_fixas', {})
        total_ferias += despesas.get('ferias', 0)
        total_inss += despesas.get('inss', 0)
        total_recisao += despesas.get('recisao', 0)
    
    print(f"Ferias: R$ {total_ferias:.2f}")
    print(f"INSS: R$ {total_inss:.2f}")
    print(f"Rescisao: R$ {total_recisao:.2f}")
    
    # Calcular mão de obra total (funcionarios + horas_extras + diaristas + ferias + inss + rescisao)
    mao_obra_total = (total_despesas['funcionarios'] + total_despesas['horas_extras'] + 
                     total_despesas['diaristas'] + total_ferias + total_inss + total_recisao)
    print(f"\nMÃO DE OBRA TOTAL (CORRIGIDA): R$ {mao_obra_total:.2f}")
    
except Exception as e:
    print(f"Erro ao conectar ao banco: {e}")
finally:
    if 'client' in locals():
        client.close()
        print("\nConexão fechada.")