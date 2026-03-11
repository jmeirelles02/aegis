import time
import logging
from src.core.interfaces.llm_gateway import LLMGateway
from src.core.interfaces.analysis_repository import AnalysisRepository
from src.core.entities.analysis_request import AnalysisRequest
from src.core.entities.analysis_result import AnalysisResult

logger = logging.getLogger(__name__)

class AnalyzeArchitectureUseCase:
    """
    Orquestra o fluxo completo de análise de arquitetura.

    Princípio SRP: apenas coordena — não analisa, não persiste diretamente.
    Princípio DIP: depende de abstrações (LLMGateway, AnalysisRepository).
    """

    def __init__(
        self,
        llm_gateway: LLMGateway,
        repository: AnalysisRepository,
    ) -> None:
        self._llm_gateway = llm_gateway
        self._repository = repository

    async def execute(self, request: AnalysisRequest) -> AnalysisResult:
        """
        Executa a análise completa:
        1. Valida o request
        2. Delega ao LLM Gateway
        3. Persiste o resultado
        4. Retorna o resultado enriquecido
        """
        logger.info(
            f"[AnalyzeArchitectureUseCase] Iniciando: '{request.title}' "
            f"| tipos: {[t.value for t in request.analysis_types]}"
        )

        start = time.monotonic()

        self._validate(request)

        result = await self._llm_gateway.analyze(request)

        saved = await self._repository.save(result)

        elapsed = int((time.monotonic() - start) * 1000)
        logger.info(
            f"[AnalyzeArchitectureUseCase] Concluído em {elapsed}ms "
            f"| score: {saved.summary.overall_score}/100 "
            f"| findings: {len(saved.findings)}"
        )

        return saved

    @staticmethod
    def _validate(request: AnalysisRequest) -> None:
        """
        Validações de negócio além das validações do Pydantic.
        Lança ValueError para casos inválidos.
        """
        if not request.description.strip():
            raise ValueError("A descrição da arquitetura não pode estar vazia.")

        if len(request.description.split()) < 10:
            raise ValueError(
                "A descrição é muito curta. "
                "Forneça mais detalhes sobre a arquitetura para uma análise precisa."
            )