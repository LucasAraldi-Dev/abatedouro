from fastapi import APIRouter

from app.api.v1.endpoints import health, lotes_abate, produtos, produto_log, despesas_padrao, abates_completos, configuracao_limites, auth

api_router = APIRouter()

api_router.include_router(health.router, prefix="/saude", tags=["saude"])
api_router.include_router(lotes_abate.router, prefix="/lotes-abate", tags=["lotes-abate"])
api_router.include_router(abates_completos.router, prefix="/abates-completos", tags=["abates-completos"])
api_router.include_router(produtos.router, prefix="/produtos", tags=["produtos"])
api_router.include_router(produto_log.router, prefix="/produto-logs", tags=["produto-logs"])
api_router.include_router(despesas_padrao.router, prefix="/despesas-padrao", tags=["despesas-padrao"])
api_router.include_router(configuracao_limites.router, prefix="/configuracao-limites", tags=["configuracao-limites"])
api_router.include_router(auth.router)