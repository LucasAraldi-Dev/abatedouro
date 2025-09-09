import asyncio
from app.core.db import get_db
from app.crud.user import get_user_crud
from app.models.user import UserPublic

async def test_me_endpoint():
    # Simular o que acontece no endpoint /auth/me
    db = await get_db()
    
    # Testar com um usuário conhecido
    username = 'lucasaraldi'
    print(f'Testando endpoint /auth/me para usuário: {username}')
    
    try:
        # Passo 1: Buscar usuário
        user = await get_user_crud(db).get_by_username(username)
        if not user:
            print('Usuário não encontrado')
            return
        
        print(f'Usuário encontrado:')
        print(f'- Type: {type(user)}')
        print(f'- Username: {user.username}')
        print(f'- Nome completo: {getattr(user, "nome_completo", "ATRIBUTO AUSENTE")}')
        print(f'- Email: {getattr(user, "email", "ATRIBUTO AUSENTE")}')
        print(f'- Is active: {user.is_active}')
        print(f'- Created at: {user.created_at}')
        
        # Passo 2: Criar UserPublic
        print('\nTentando criar UserPublic...')
        user_public = UserPublic(
            username=user.username,
            nome_completo=user.nome_completo,
            email=user.email,
            is_active=user.is_active,
            created_at=user.created_at
        )
        print('UserPublic criado com sucesso!')
        print(f'- Username: {user_public.username}')
        print(f'- Nome completo: {user_public.nome_completo}')
        print(f'- Email: {user_public.email}')
        print(f'- Is active: {user_public.is_active}')
        print(f'- Created at: {user_public.created_at}')
        
    except Exception as e:
        print(f'Erro: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_me_endpoint())