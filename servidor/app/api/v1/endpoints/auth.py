from fastapi import APIRouter, Depends, HTTPException, Response, Request, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.db import get_db
from app.core.config import settings
from app.crud.user import get_user_crud
from app.models.user import UserCreate, UserPublic
from app.utils.security import create_access_token, decode_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
  crud = get_user_crud(db)
  try:
    created = await crud.create(user_in)
    return created
  except ValueError as e:
    raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
async def login(data: dict, response: Response, db: AsyncIOMotorDatabase = Depends(get_db)):
  username = data.get("username")
  password = data.get("password")
  if not username or not password:
    raise HTTPException(status_code=400, detail="Credenciais inválidas")

  crud = get_user_crud(db)
  user = await crud.authenticate(username, password)
  if not user:
    raise HTTPException(status_code=401, detail="Usuário ou senha incorretos")
  if not user.is_active:
    raise HTTPException(status_code=403, detail="Conta inativa")

  token = create_access_token(subject=user.username)
  # Ajuste de SameSite para produção (cross-site): usar 'none' quando COOKIE_SECURE=true
  samesite_value = "none" if settings.COOKIE_SECURE else "lax"
  cookie_params = {
    "key": "session",
    "value": token,
    "httponly": True,
    "secure": settings.COOKIE_SECURE,
    "samesite": samesite_value,
    "path": "/",
    "max_age": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
  }
  response.set_cookie(**cookie_params)
  return {"message": "Login efetuado"}


@router.post("/logout")
async def logout(response: Response):
  # Importante: para que os navegadores aceitem a remoção do cookie em contexto cross-site,
  # é necessário enviar os mesmos atributos (SameSite/Secure/Path) usados no set_cookie.
  samesite_value = "none" if settings.COOKIE_SECURE else "lax"
  response.delete_cookie(
    key="session",
    path="/",
    secure=settings.COOKIE_SECURE,
    samesite=samesite_value,
  )
  return {"message": "Logout efetuado"}


@router.get("/me", response_model=UserPublic)
async def me(request: Request, db: AsyncIOMotorDatabase = Depends(get_db)):
  token = request.cookies.get("session")
  if not token:
    raise HTTPException(status_code=401, detail="Não autenticado")
  username = decode_access_token(token)
  if not username:
    raise HTTPException(status_code=401, detail="Token inválido")
  user = await get_user_crud(db).get_by_username(username)
  if not user:
    raise HTTPException(status_code=404, detail="Usuário não encontrado")
  # Retornar todos os campos exigidos por UserPublic
  return UserPublic(
    username=user.username,
    nome_completo=user.nome_completo,
    email=user.email,
    is_active=user.is_active,
    created_at=user.created_at
  )