from typing import TypedDict, Annotated
from operator import add
from src.core.entities.analysis_request import AnalysisRequest
from src.core.entities.analysis_result import Finding, AnalysisSummary


class AegisState(TypedDict):
    """
    Estado compartilhado entre todos os nós do grafo.

    raw_findings  → acumula com Annotated[list, add] (nós paralelos)
    findings      → lista final após deduplicação (aggregator_node)
    """
    request: AnalysisRequest

    active_analysis_types: list[str]
    current_step: str
    errors: Annotated[list[str], add]

    raw_findings: Annotated[list[Finding], add]

    findings: list[Finding]

    summary: AnalysisSummary | None
    processing_time_ms: int