from typing import Optional
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from passlib.context import CryptContext

from app.models.user import UserCreate, UserInDB, UserPublic

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


class CRUDUser:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.usuarios

    async def get_by_username(self, username: str) -> Optional[UserInDB]:
        user = await self.collection.find_one({"username": username})
        return UserInDB(**user) if user else None

    async def create(self, user_data: UserCreate) -> UserPublic:
        # Verificar se usuário já existe
        existing_user = await self.collection.find_one({
            "$or": [
                {"username": user_data.username},
                {"email": str(user_data.email)}
            ]
        })
        if existing_user:
            if existing_user["username"] == user_data.username:
                raise ValueError("Nome de usuário já existe")
            else:
                raise ValueError("Email já está em uso")
        user_doc = {
            "username": user_data.username,
            "nome_completo": user_data.nome_completo,
            "email": str(user_data.email),
            "password_hash": hash_password(user_data.password),
            "is_active": False,
            "created_at": datetime.utcnow(),
        }
        result = await self.collection.insert_one(user_doc)
        created = await self.collection.find_one({"_id": result.inserted_id})
        # Não retornar hash
        return UserPublic(
            username=created["username"],
            nome_completo=created["nome_completo"],
            email=created["email"],
            is_active=created["is_active"],
            created_at=created["created_at"]
        ) 

    async def authenticate(self, username: str, password: str) -> Optional[UserInDB]:
        user = await self.collection.find_one({"username": username})
        if not user:
            return None
        if not verify_password(password, user.get("password_hash", "")):
            return None
        return UserInDB(
            id=user.get("_id"),
            username=user["username"],
            nome_completo=user["nome_completo"],
            email=user["email"],
            password_hash=user["password_hash"],
            is_active=user["is_active"],
            created_at=user["created_at"]
        )


def get_user_crud(db: AsyncIOMotorDatabase) -> CRUDUser:
    return CRUDUser(db)