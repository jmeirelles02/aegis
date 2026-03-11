import logging
from src.core.interfaces.analysis_repository import AnalysisRepository
from src.core.entities.analysis_result import AnalysisResult

logger = logging.getLogger(__name__)


class InMemoryAnalysisRepository(AnalysisRepository):
    """
    Implementação in-memory do repositório.
    Perfeito para desenvolvimento — sem dependências externas.
    Princípio DIP: implementa o contrato definido no core.
    """

    def __init__(self) -> None:
        self._store: dict[str, AnalysisResult] = {}
        logger.info("InMemoryAnalysisRepository inicializado.")

    async def save(self, result: AnalysisResult) -> AnalysisResult:
        self._store[result.id] = result
        logger.info(f"[Repository] Salvo: {result.id}")
        return result

    async def find_by_id(self, id: str) -> AnalysisResult | None:
        result = self._store.get(id)
        if result:
            logger.info(f"[Repository] Encontrado: {id}")
        else:
            logger.warning(f"[Repository] Não encontrado: {id}")
        return result

    async def list_all(self) -> list[AnalysisResult]:
        results = list(self._store.values())
        logger.info(f"[Repository] Listando {len(results)} análises.")
        return results