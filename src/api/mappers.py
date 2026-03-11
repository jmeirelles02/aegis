# src/api/mappers.py

from src.core.entities.analysis_result import AnalysisResult
from src.api.schemas import (
    AnalysisResponse,
    FindingResponse,
    SummaryResponse,
)


def to_analysis_response(result: AnalysisResult) -> AnalysisResponse:
    """Converte entidade de domínio → schema de resposta da API."""
    return AnalysisResponse(
        id=result.id,
        request_title=result.request_title,
        analysis_types=result.analysis_types,
        findings=[
            FindingResponse(
                severity=f.severity,
                category=f.category,
                title=f.title,
                description=f.description,
                recommendation=f.recommendation,
                code_example=f.code_example,
            )
            for f in result.findings
        ],
        summary=SummaryResponse(
            overall_score=result.summary.overall_score,
            strengths=result.summary.strengths,
            critical_issues=result.summary.critical_issues,
            quick_wins=result.summary.quick_wins,
            verdict=result.summary.verdict,
        ),
        has_critical_issues=result.has_critical_issues,
        processing_time_ms=result.processing_time_ms,
        created_at=result.created_at,
    )