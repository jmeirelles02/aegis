# main.py  (na raiz do projeto)

import logging
import uvicorn
from src.config.settings import settings

logging.basicConfig(
    level=logging.DEBUG if settings.app_debug else logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

if __name__ == "__main__":
    uvicorn.run(
        "src.api.app:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.app_debug,
        log_level="debug" if settings.app_debug else "info",
    )