from abc import ABC, abstractmethod
from src.core.entities.analysis_request import AnalysisRequest
from src.core.entities.analysis_result import AnalysisResult

class LLMGateway(ABC):
    """
    Contrato para qualquer provedor de LLM.
    Princípio DIP: o core depende desta abstração,
    nunca da implementação concreta (Gemini, OpenAI, etc.)
    """

    @abstractmethod
    async def analyze(self, request: AnalysisRequest) -> AnalysisResult:
        """Executa a análise de arquitetura via LLM."""
        ...

    @abstractmethod
    async def health_check(self) -> bool:
        """Verifica se o LLM está acessível."""
        ...