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
    # Input
    request: AnalysisRequest

    # Controle de fluxo
    active_analysis_types: list[str]
    current_step: str
    errors: Annotated[list[str], add]

    # Findings BRUTOS dos nós paralelos (acumulados via add)
    raw_findings: Annotated[list[Finding], add]

    # Findings FINAIS após deduplicação (substitui, não acumula)
    findings: list[Finding]

    # Output final
    summary: AnalysisSummary | None
    processing_time_ms: int