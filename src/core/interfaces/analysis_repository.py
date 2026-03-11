from abc import ABC, abstractmethod
from src.core.entities.analysis_result import AnalysisResult

class AnalysisRepository(ABC):
    """
    Contrato para persistência de análises.
    Hoje: in-memory | Amanhã: PostgreSQL, MongoDB — sem mudar o core.
    """

    @abstractmethod
    async def save(self, result: AnalysisResult) -> AnalysisResult:
        ...

    @abstractmethod
    async def find_by_id(self, id: str) -> AnalysisResult | None:
        ...

    @abstractmethod
    async def list_all(self) -> list[AnalysisResult]:
        ...