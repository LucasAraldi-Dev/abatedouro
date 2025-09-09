import asyncio
from app.core.db import get_client
from app.crud.user import verify_password

async def check_password():
    client = await get_client()
    db = client.abatedouro
    
    # Buscar o usuário
    user = await db.usuarios.find_one({"username": "lucasaraldi"})
    if user:
        print(f'Usuário encontrado: {user["username"]}')
        print(f'Password hash: {user.get("password_hash", "N/A")}')
        
        # Testar algumas senhas comuns
        test_passwords = ["123456", "password", "admin", "lucasaraldi", "123"]
        
        for pwd in test_passwords:
            try:
                is_valid = verify_password(pwd, user["password_hash"])
                print(f'Senha "{pwd}": {"VÁLIDA" if is_valid else "inválida"}')
                if is_valid:
                    break
            except Exception as e:
                print(f'Erro ao verificar senha "{pwd}": {e}')
    else:
        print('Usuário não encontrado')
    
    client.close()

if __name__ == "__main__":
    asyncio.run(check_password())