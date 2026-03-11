import logging
from src.core.interfaces.analysis_repository import AnalysisRepository
from src.core.entities.analysis_result import AnalysisResult

logger = logging.getLogger(__name__)

class ListAnalysesUseCase:
    """
    Lista todas as análises realizadas.
    """

    def __init__(self, repository: AnalysisRepository) -> None:
        self._repository = repository

    async def execute(self) -> list[AnalysisResult]:
        results = await self._repository.list_all()
        logger.info(f"[ListAnalysesUseCase] {len(results)} análises encontradas.")
        return results