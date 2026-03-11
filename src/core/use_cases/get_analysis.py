import logging
from src.core.interfaces.analysis_repository import AnalysisRepository
from src.core.entities.analysis_result import AnalysisResult

logger = logging.getLogger(__name__)

class GetAnalysisUseCase:
    """
    Recupera uma análise existente pelo ID.
    Princípio SRP: apenas leitura, sem lógica de negócio adicional.
    """

    def __init__(self, repository: AnalysisRepository) -> None:
        self._repository = repository

    async def execute(self, analysis_id: str) -> AnalysisResult:
        """
        Busca análise por ID.
        Lança ValueError se não encontrada.
        """
        if not analysis_id or not analysis_id.strip():
            raise ValueError("ID da análise não pode estar vazio.")

        result = await self._repository.find_by_id(analysis_id)

        if result is None:
            raise ValueError(f"Análise '{analysis_id}' não encontrada.")

        logger.info(f"[GetAnalysisUseCase] Recuperado: {analysis_id}")
        return result