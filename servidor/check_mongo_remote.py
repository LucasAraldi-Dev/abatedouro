import pymongo
from datetime import datetime

# Conectar ao MongoDB remoto
client = pymongo.MongoClient('mongodb://lucasaraldi:R6pXvaislUmmKm8A@ac-nqlllrv-shard-00-00.tvwmq9c.mongodb.net:27017,ac-nqlllrv-shard-00-01.tvwmq9c.mongodb.net:27017,ac-nqlllrv-shard-00-02.tvwmq9c.mongodb.net:27017/abatedouro?ssl=true&authSource=admin&retryWrites=true&w=majority')

db = client['abatedouro']

print("=== VERIFICAÇÃO DO BANCO REMOTO ===")
print(f"Lotes: {db.lotes_abate.count_documents({})}")
print(f"Abates Completos: {db.abates_completos.count_documents({})}")
print(f"Produtos: {db.produtos.count_documents({})}")

print("\n=== LOTES ENCONTRADOS ===")
lotes = list(db.lotes_abate.find({}, {'_id': 0, 'data_abate': 1, 'quantidade_aves': 1, 'peso_total_kg': 1, 'tipo_ave': 1}))
for i, lote in enumerate(lotes, 1):
    print(f"{i}. Data: {lote.get('data_abate')}, Aves: {lote.get('quantidade_aves')}, Peso: {lote.get('peso_total_kg')}kg, Tipo: {lote.get('tipo_ave')}")

print("\n=== ABATES COMPLETOS ENCONTRADOS ===")
abates = list(db.abates_completos.find({}, {'_id': 0, 'data_abate': 1, 'lucro_liquido': 1, 'rendimento_final': 1, 'eficiencia_operacional': 1, 'score_performance': 1}))
for i, abate in enumerate(abates, 1):
    print(f"{i}. Data: {abate.get('data_abate')}")
    print(f"   Lucro Líquido: {abate.get('lucro_liquido')}")
    print(f"   Rendimento Final: {abate.get('rendimento_final')}")
    print(f"   Eficiência Operacional: {abate.get('eficiencia_operacional')}")
    print(f"   Score Performance: {abate.get('score_performance')}")
    print()

client.close()
print("Conexão fechada.")