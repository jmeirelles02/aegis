import json
import time
import logging
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from src.core.interfaces.llm_gateway import LLMGateway
from src.core.entities.analysis_request import AnalysisRequest, AnalysisType
from src.core.entities.analysis_result import (
    AnalysisResult,
    Finding,
    AnalysisSummary,
    SeverityLevel,
)
from src.config.settings import settings
from src.infrastructure.llm.prompts import PROMPT_REGISTRY
from src.infrastructure.llm.prompts.base import BASE_SYSTEM_PROMPT

logger = logging.getLogger(__name__)

class GeminiClient(LLMGateway):
    """
    Implementação concreta do LLMGateway usando Google Gemini.
    Princípio DIP: o core nunca importa esta classe diretamente.
    """

    def __init__(self) -> None:
        self._llm = ChatGoogleGenerativeAI(
            model=settings.gemini_model,
            google_api_key=settings.google_api_key,
            temperature=settings.llm_temperature,
            max_output_tokens=settings.llm_max_tokens,
        )
        logger.info(f"GeminiClient inicializado com modelo: {settings.gemini_model}")

    async def analyze(self, request: AnalysisRequest) -> AnalysisResult:
        start_time = time.monotonic()
        all_findings: list[Finding] = []
        raw_responses: list[str] = []

        for analysis_type in request.analysis_types:
            logger.info(f"Executando análise: {analysis_type.value}")

            findings, raw = await self._run_single_analysis(
                request=request,
                analysis_type=analysis_type,
            )
            all_findings.extend(findings)
            raw_responses.append(f"[{analysis_type.value}]\n{raw}")

        summary = await self._generate_summary(
            request=request,
            findings=all_findings,
        )

        elapsed_ms = int((time.monotonic() - start_time) * 1000)

        return AnalysisResult(
            request_title=request.title,
            analysis_types=[t.value for t in request.analysis_types],
            findings=all_findings,
            summary=summary,
            raw_response="\n\n".join(raw_responses),
            processing_time_ms=elapsed_ms,
        )

    async def _run_single_analysis(
        self,
        request: AnalysisRequest,
        analysis_type: AnalysisType,
    ) -> tuple[list[Finding], str]:
        """Executa um único tipo de análise."""
        prompt_template = PROMPT_REGISTRY[analysis_type]

        human_message = prompt_template.format(
            title=request.title,
            description=request.description,
            context=json.dumps(request.context, ensure_ascii=False),
            depth=request.depth.value,
        )

        messages = [
            SystemMessage(content=BASE_SYSTEM_PROMPT),
            HumanMessage(content=human_message),
        ]

        response = await self._llm.ainvoke(messages)

        raw_content = self._extract_text(response.content)

        findings = self._parse_findings(raw_content, analysis_type)
        return findings, raw_content

    async def _generate_summary(
        self,
        request: AnalysisRequest,
        findings: list[Finding],
    ) -> AnalysisSummary:
        """Gera o summary consolidado baseado em todos os findings."""
        findings_text = "\n".join(
            f"- [{f.severity.value.upper()}] {f.category}: {f.title}"
            for f in findings
        )

        summary_prompt = f"""
Com base nos seguintes findings de uma análise de arquitetura:

{findings_text}

Para o sistema: {request.title}

Retorne um JSON com este schema exato:
{{
    "overall_score": 0-100,
    "strengths": ["lista de pontos fortes identificados"],
    "critical_issues": {sum(1 for f in findings if f.severity == SeverityLevel.CRITICAL)},
    "quick_wins": ["lista de melhorias rápidas de alto impacto"],
    "verdict": "veredicto final em 2-3 frases como Shadow Architect"
}}

Retorne APENAS o JSON, sem texto adicional.
"""
        messages = [
            SystemMessage(content=BASE_SYSTEM_PROMPT),
            HumanMessage(content=summary_prompt),
        ]

        response = await self._llm.ainvoke(messages)

        raw = self._extract_text(response.content)

        return self._parse_summary(raw, findings)

    async def health_check(self) -> bool:
        """Testa conectividade com o Gemini."""
        try:
            response = await self._llm.ainvoke(
                [HumanMessage(content="Responda apenas: OK")]
            )
            content = self._extract_text(response.content)
            return "OK" in content

        except Exception as e:
            error_str = str(e)

            if "RESOURCE_EXHAUSTED" in error_str or "429" in error_str:
                logger.error(
                    "❌ Cota da API esgotada! "
                    "Troque o modelo no .env para 'gemini-1.5-flash' "
                    "ou aguarde o reset da cota."
                )
            elif "API_KEY" in error_str or "401" in error_str:
                logger.error(
                    "❌ API Key inválida! "
                    "Verifique o valor de GOOGLE_API_KEY no .env"
                )
            elif "404" in error_str:
                logger.error(
                    f"❌ Modelo '{settings.gemini_model}' não encontrado! "
                    "Verifique o valor de GEMINI_MODEL no .env"
                )
            else:
                logger.error(f"Health check falhou: {e}")

            return False

    @staticmethod
    def _extract_text(content: object) -> str:
        """
        ✅ NOVO MÉTODO — Extrai texto do content independente do formato.

        O Gemini pode retornar:
        - str: "{ ... }"
        - list: [{'type': 'text', 'text': '{ ... }'}]
        """
        if isinstance(content, str):
            return content

        if isinstance(content, list):
            texts = []
            for item in content:
                if isinstance(item, dict) and item.get("type") == "text":
                    texts.append(item.get("text", ""))
                elif isinstance(item, str):
                    texts.append(item)
            return "\n".join(texts)

        return str(content)

    @staticmethod
    def _clean_json(raw: str) -> str:
        """
        Remove markdown code blocks se o LLM os incluir.
        Ex: ```json { ... } ``` → { ... }
        """
        clean = raw.strip()

        if clean.startswith("```"):
            lines = clean.split("\n")
            clean = "\n".join(lines[1:-1]).strip()

        return clean

    def _parse_findings(
        self,
        raw_content: str,
        analysis_type: AnalysisType,
    ) -> list[Finding]:
        """Parse seguro da resposta do LLM para findings."""
        try:
            clean = self._clean_json(raw_content)
            data = json.loads(clean)

            return [
                Finding(
                    severity=SeverityLevel(f.get("severity", "info")),
                    category=f.get("category", analysis_type.value),
                    title=f.get("title", "Sem título"),
                    description=f.get("description", ""),
                    recommendation=f.get("recommendation", ""),
                    code_example=f.get("code_example"),
                )
                for f in data.get("findings", [])
            ]
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            logger.warning(f"Falha ao parsear findings: {e}")
            return self._fallback_finding(analysis_type, raw_content)

    def _parse_summary(
        self,
        raw_content: str,
        findings: list[Finding],
    ) -> AnalysisSummary:
        """Parse seguro do summary."""
        try:
            clean = self._clean_json(raw_content)
            data = json.loads(clean)

            return AnalysisSummary(
                overall_score=int(data.get("overall_score", 50)),
                strengths=data.get("strengths", []),
                critical_issues=sum(
                    1 for f in findings
                    if f.severity == SeverityLevel.CRITICAL
                ),
                quick_wins=data.get("quick_wins", []),
                verdict=data.get("verdict", "Análise concluída."),
            )
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            logger.warning(f"Falha ao parsear summary: {e}")
            return self._fallback_summary(findings)

    @staticmethod
    def _fallback_finding(
        analysis_type: AnalysisType,
        raw_content: str,
    ) -> list[Finding]:
        """Finding de fallback quando o parse falha."""
        return [
            Finding(
                severity=SeverityLevel.INFO,
                category=analysis_type.value,
                title="Resposta não estruturada",
                description=raw_content[:500],
                recommendation="Tente reformular a descrição da arquitetura.",
            )
        ]

    @staticmethod
    def _fallback_summary(findings: list[Finding]) -> AnalysisSummary:
        """Summary de fallback."""
        critical = sum(
            1 for f in findings
            if f.severity == SeverityLevel.CRITICAL
        )
        return AnalysisSummary(
            overall_score=50,
            strengths=["Análise parcialmente concluída"],
            critical_issues=critical,
            quick_wins=[],
            verdict="Não foi possível gerar o sumário completo. Verifique os findings individuais.",
        )