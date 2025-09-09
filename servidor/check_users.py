import asyncio
from app.core.db import get_client
from app.models.user import UserInDB
from app.crud.user import CRUDUser

async def check_users():
    client = await get_client()
    db = client.abatedouro
    
    # Verificar dados brutos do MongoDB
    users = await db.usuarios.find().to_list(length=10)
    print('=== DADOS BRUTOS DO MONGODB ===')
    for user in users:
        print(f'- Username: {user.get("username", "N/A")}')
        print(f'  Nome completo: {user.get("nome_completo", "CAMPO AUSENTE")}')
        print(f'  Email: {user.get("email", "CAMPO AUSENTE")}')
        print(f'  Is active: {user.get("is_active", "N/A")}')
        print(f'  Created at: {user.get("created_at", "N/A")}')
        print('---')
    
    # Testar o CRUD
    print('\n=== TESTANDO CRUD get_by_username ===')
    crud = CRUDUser(db)
    try:
        user_obj = await crud.get_by_username('lucasaraldi')
        if user_obj:
            print(f'UserInDB object criado com sucesso:')
            print(f'- Username: {user_obj.username}')
            print(f'- Nome completo: {getattr(user_obj, "nome_completo", "ATRIBUTO AUSENTE")}')
            print(f'- Email: {getattr(user_obj, "email", "ATRIBUTO AUSENTE")}')
            print(f'- Is active: {user_obj.is_active}')
            print(f'- Created at: {user_obj.created_at}')
        else:
            print('Usuário não encontrado pelo CRUD')
    except Exception as e:
        print(f'Erro ao criar UserInDB: {e}')
    
    client.close()

if __name__ == "__main__":
    asyncio.run(check_users())