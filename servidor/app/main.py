from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings

app = FastAPI(title=settings.APP_NAME)

# Debug: Log das configurações CORS
print(f"BACKEND_CORS_ORIGINS (raw): {settings.BACKEND_CORS_ORIGINS}")
print(f"CORS origins (parsed): {settings.cors_origins}")

# CORS
origins = settings.cors_origins
if origins:
    print(f"Aplicando middleware CORS com origins: {origins}")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    print("AVISO: Nenhuma origin CORS configurada!")

# Compat: rota antiga
@app.get("/saude")
async def saude_compat():
    return {"status": "ok"}

# API v1 - importar e incluir após a criação da app
from app.api.v1.api import api_router
app.include_router(api_router, prefix=settings.API_V1_STR)

print(f"App criada com {len(app.routes)} rotas")
for route in app.routes:
    if hasattr(route, 'methods') and hasattr(route, 'path'):
        print(f"  {route.methods} {route.path}")