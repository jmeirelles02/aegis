# src/api/routes/health.py

from fastapi import APIRouter
from src.api.schemas import HealthResponse
from src.core.dependencies import get_llm_gateway
from src.config.settings import settings

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
)
async def health_check() -> HealthResponse:
    """Verifica se o serviço e o LLM estão operacionais."""
    gateway = get_llm_gateway()
    llm_ok = await gateway.health_check()

    return HealthResponse(
        status="healthy" if llm_ok else "degraded",
        llm_available=llm_ok,
    )