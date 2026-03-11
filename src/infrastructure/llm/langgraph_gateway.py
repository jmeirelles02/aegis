import time
import logging
from src.core.interfaces.llm_gateway import LLMGateway
from src.core.entities.analysis_request import AnalysisRequest
from src.core.entities.analysis_result import AnalysisResult, AnalysisSummary
from src.infrastructure.graph.aegis_graph import get_aegis_graph
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from src.config.settings import settings

logger = logging.getLogger(__name__)


class LangGraphGateway(LLMGateway):
    """
    Implementação do LLMGateway usando o grafo LangGraph.
    Substitui o GeminiClient direto — agora usa o pipeline completo.
    """

    def __init__(self) -> None:
        self._graph = get_aegis_graph()
        self._llm = ChatGoogleGenerativeAI(
            model=settings.gemini_model,
            google_api_key=settings.google_api_key,
            temperature=settings.llm_temperature,
        )
        logger.info("LangGraphGateway inicializado.")

    async def analyze(self, request: AnalysisRequest) -> AnalysisResult:
        """Executa o pipeline completo via LangGraph."""
        start = time.monotonic()

        initial_state = {"request": request}
        final_state = await self._graph.ainvoke(initial_state)

        elapsed_ms = int((time.monotonic() - start) * 1000)

        findings = final_state.get("findings", [])
        summary: AnalysisSummary = final_state.get("summary")

        if summary is None:
            from src.core.entities.analysis_result import SeverityLevel
            summary = AnalysisSummary(
                overall_score=0,
                strengths=[],
                critical_issues=sum(
                    1 for f in findings
                    if f.severity == SeverityLevel.CRITICAL
                ),
                quick_wins=[],
                verdict="Erro ao gerar sumário.",
            )

        return AnalysisResult(
            request_title=request.title,
            analysis_types=[t.value for t in request.analysis_types],
            findings=findings,
            summary=summary,
            raw_response=str(final_state.get("raw_findings", [])),
            processing_time_ms=elapsed_ms,
        )

    async def health_check(self) -> bool:
        """Testa conectividade com o Gemini."""
        try:
            response = await self._llm.ainvoke(
                [HumanMessage(content="Responda apenas: OK")]
            )
            content = response.content
            if isinstance(content, list):
                content = " ".join(
                    i.get("text", "") if isinstance(i, dict) else str(i)
                    for i in content
                )
            return "OK" in str(content)
        except Exception as e:
            logger.error(f"Health check falhou: {e}")
            return False