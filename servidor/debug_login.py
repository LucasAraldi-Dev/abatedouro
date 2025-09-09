import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from app.crud.user import get_user_crud, verify_password

async def debug_login():
    # Conectar ao MongoDB
    client = AsyncIOMotorClient(settings.MONGODB_URI)
    db = client[settings.MONGODB_DBNAME]
    
    print("=== DEBUG LOGIN TESTUSER ===")
    
    # Buscar usuário diretamente no banco
    user_doc = await db.users.find_one({"username": "testuser"})
    if not user_doc:
        print("❌ Usuário testuser não encontrado no banco")
        return
    
    print(f"✅ Usuário encontrado:")
    print(f"  - Username: {user_doc['username']}")
    print(f"  - Nome: {user_doc['nome_completo']}")
    print(f"  - Email: {user_doc['email']}")
    print(f"  - Ativo: {user_doc['is_active']}")
    print(f"  - Hash da senha: {user_doc['password_hash'][:20]}...")
    
    # Testar verificação de senha
    password = "testpass123"
    print(f"\n=== TESTANDO SENHA '{password}' ===")
    
    try:
        is_valid = verify_password(password, user_doc['password_hash'])
        print(f"✅ Resultado verify_password: {is_valid}")
    except Exception as e:
        print(f"❌ Erro na verify_password: {e}")
    
    # Testar CRUD authenticate
    print(f"\n=== TESTANDO CRUD AUTHENTICATE ===")
    crud = get_user_crud(db)
    
    try:
        authenticated_user = await crud.authenticate("testuser", password)
        if authenticated_user:
            print(f"✅ Autenticação bem-sucedida:")
            print(f"  - Username: {authenticated_user.username}")
            print(f"  - Nome: {authenticated_user.nome_completo}")
            print(f"  - Ativo: {authenticated_user.is_active}")
        else:
            print(f"❌ Autenticação falhou - retornou None")
    except Exception as e:
        print(f"❌ Erro na autenticação: {e}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(debug_login())