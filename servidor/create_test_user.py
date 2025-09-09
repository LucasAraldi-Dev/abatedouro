import asyncio
from app.core.db import get_db
from app.crud.user import CRUDUser, hash_password
from app.models.user import UserCreate
from datetime import datetime

async def create_test_user():
    db = await get_db()
    
    # Criar usuário de teste
    test_user_data = {
        "username": "testuser",
        "nome_completo": "Usuario de Teste",
        "email": "test@example.com",
        "password": "testpass123",
        "confirm_password": "testpass123"
    }
    
    try:
        # Verificar se já existe
        existing = await db.usuarios.find_one({"username": "testuser"})
        if existing:
            print("Usuário de teste já existe, removendo...")
            await db.usuarios.delete_one({"username": "testuser"})
        
        # Criar novo usuário diretamente no banco
        user_doc = {
            "username": test_user_data["username"],
            "nome_completo": test_user_data["nome_completo"],
            "email": test_user_data["email"],
            "password_hash": hash_password(test_user_data["password"]),
            "is_active": True,
            "created_at": datetime.utcnow()
        }
        
        result = await db.usuarios.insert_one(user_doc)
        print(f"Usuário de teste criado com ID: {result.inserted_id}")
        print(f"Username: {test_user_data['username']}")
        print(f"Password: {test_user_data['password']}")
        print(f"Nome completo: {test_user_data['nome_completo']}")
        print(f"Email: {test_user_data['email']}")
        
    except Exception as e:
        print(f"Erro ao criar usuário de teste: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(create_test_user())