from fastapi import APIRouter

router = APIRouter()

@router.get("/", summary="Status da API")
async def health():
    return {"status": "ok"}