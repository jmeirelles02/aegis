import logging
from contextlib import asynccontextmanager
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

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        logger.info(f"🛡️  {settings.app_name} iniciando...")
        logger.info(f"   Ambiente: {settings.app_env}")
        logger.info(f"   Modelo LLM: {settings.gemini_model}")
        logger.info(f"   Docs: http://{settings.app_host}:{settings.app_port}/docs")
        yield
        logger.info("🛡️  Aegis encerrando...")

    app = FastAPI(
        title=settings.app_name,
        description=(
            "Aegis\n\n"
            "Analisa propostas de arquitetura de software com foco em "
            "escalabilidade, segurança, SOLID e Clean Architecture."
        ),
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        debug=settings.app_debug,
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"] if not settings.is_production else [],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_exception_handler(Exception, global_error_handler)

    app.include_router(health.router)
    app.include_router(analysis.router)

    return app


app = create_app()