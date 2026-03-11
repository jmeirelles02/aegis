import json
import logging
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

from src.infrastructure.graph.state import AegisState
from src.infrastructure.llm.prompts.base import BASE_SYSTEM_PROMPT
from src.core.entities.analysis_result import AnalysisSummary, SeverityLevel
from src.config.settings import settings

logger = logging.getLogger(__name__)


async def summary_node(state: AegisState) -> dict:
    """Gera o veredicto final como Shadow Architect."""

    findings = state.get("findings", [])
    request = state["request"]

    findings_text = "\n".join(
        f"- [{f.severity.value.upper()}] {f.category}: {f.title}"
        for f in findings
    ) or "Nenhum finding encontrado."

    critical_count = sum(
        1 for f in findings
        if f.severity == SeverityLevel.CRITICAL
    )

    prompt = f"""
Como Shadow Architect, analise os findings abaixo e gere um summary executivo.

Sistema: {request.title}
Total de findings: {len(findings)}
Issues críticos: {critical_count}

Findings:
{findings_text}

Retorne APENAS este JSON:
{{
    "overall_score": <inteiro de 0 a 100>,
    "strengths": ["ponto forte 1", "ponto forte 2"],
    "critical_issues": {critical_count},
    "quick_wins": ["melhoria rápida 1", "melhoria rápida 2"],
    "verdict": "veredicto em 2-3 frases diretas e técnicas"
}}
"""
    llm = ChatGoogleGenerativeAI(
        model=settings.gemini_model,
        google_api_key=settings.google_api_key,
        temperature=0.2,
        max_output_tokens=1024,
    )

    try:
        response = await llm.ainvoke([
            SystemMessage(content=BASE_SYSTEM_PROMPT),
            HumanMessage(content=prompt),
        ])

        raw = _extract_text(response.content)
        clean = _clean_json(raw)
        data = json.loads(clean)

        summary = AnalysisSummary(
            overall_score=int(data.get("overall_score", 50)),
            strengths=data.get("strengths", []),
            critical_issues=critical_count,
            quick_wins=data.get("quick_wins", []),
            verdict=data.get("verdict", "Análise concluída."),
        )

    except Exception as e:
        logger.error(f"[summary_node] Erro: {e}")
        summary = AnalysisSummary(
            overall_score=50,
            strengths=[],
            critical_issues=critical_count,
            quick_wins=[],
            verdict="Erro ao gerar sumário. Verifique os findings individuais.",
        )

    logger.info(f"[summary_node] Score final: {summary.overall_score}/100")
    return {
        "summary": summary,
        "current_step": "done",
    }


def _extract_text(content: object) -> str:
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


def _clean_json(raw: str) -> str:
    clean = raw.strip()
    if clean.startswith("```"):
        lines = clean.split("\n")
        clean = "\n".join(lines[1:-1]).strip()
    return clean