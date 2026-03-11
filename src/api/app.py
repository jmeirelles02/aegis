# src/api/app.py

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import health, analysis
from src.api.middlewares.error_handler import global_error_handler
from src.config.settings import settings

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """
    Factory da aplicação FastAPI.
    Princípio SRP: configuração centralizada e testável.
    """
    app = FastAPI(
        title=settings.app_name,
        description=(
            "🛡️ Aegis — Shadow Architect\n\n"
            "Analisa propostas de arquitetura de software com foco em "
            "escalabilidade, segurança, SOLID e Clean Architecture."
        ),
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        debug=settings.app_debug,
    )

    # ── CORS ────────────────────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"] if not settings.is_production else [],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── Error Handler Global ─────────────────────────────────────
    app.add_exception_handler(Exception, global_error_handler)

    # ── Rotas ────────────────────────────────────────────────────
    app.include_router(health.router)
    app.include_router(analysis.router)

    # ── Eventos ──────────────────────────────────────────────────
    @app.on_event("startup")
    async def on_startup() -> None:
        logger.info(f"🛡️  {settings.app_name} iniciando...")
        logger.info(f"   Ambiente: {settings.app_env}")
        logger.info(f"   Modelo LLM: {settings.gemini_model}")
        logger.info(f"   Docs: http://{settings.app_host}:{settings.app_port}/docs")

    @app.on_event("shutdown")
    async def on_shutdown() -> None:
        logger.info("🛡️  Aegis encerrando...")

    return app


app = create_app()