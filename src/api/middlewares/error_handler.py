import logging
from fastapi import Request, status
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

async def global_error_handler(request: Request, exc: Exception) -> JSONResponse:
    """Captura erros não tratados e retorna resposta padronizada."""
    logger.error(
        f"Erro não tratado: {exc} "
        f"| method={request.method} "
        f"| path={request.url.path}"
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "detail": str(exc),
        },
    )