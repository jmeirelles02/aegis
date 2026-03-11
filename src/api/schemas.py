from pydantic import BaseModel, Field
from datetime import datetime
from src.core.entities.analysis_request import AnalysisType, AnalysisDepth
from src.core.entities.analysis_result import SeverityLevel


class AnalysisRequestSchema(BaseModel):
    """Schema de entrada da API."""
    title: str = Field(
        ...,
        min_length=3,
        max_length=200,
        examples=["API de Pagamentos com Microserviços"],
    )
    description: str = Field(
        ...,
        min_length=20,
        max_length=10_000,
        examples=["Sistema distribuído com Kafka e Redis..."],
    )
    analysis_types: list[AnalysisType] = Field(
        default=[AnalysisType.ARCHITECTURE],
    )
    depth: AnalysisDepth = Field(default=AnalysisDepth.STANDARD)
    context: dict[str, str] = Field(default_factory=dict)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "API de E-commerce",
                "description": "Monolito FastAPI com PostgreSQL, sem cache, sem filas.",
                "analysis_types": ["architecture", "security"],
                "depth": "standard",
                "context": {"language": "Python", "scale": "10k users"},
            }
        }
    }


class FindingResponse(BaseModel):
    severity: SeverityLevel
    category: str
    title: str
    description: str
    recommendation: str
    code_example: str | None = None


class SummaryResponse(BaseModel):
    overall_score: int
    strengths: list[str]
    critical_issues: int
    quick_wins: list[str]
    verdict: str


class AnalysisResponse(BaseModel):
    id: str
    request_title: str
    analysis_types: list[str]
    findings: list[FindingResponse]
    summary: SummaryResponse
    has_critical_issues: bool
    processing_time_ms: int
    created_at: datetime


class AnalysisListResponse(BaseModel):
    total: int
    analyses: list[AnalysisResponse]


class HealthResponse(BaseModel):
    status: str
    llm_available: bool
    version: str = "1.0.0"


class ErrorResponse(BaseModel):
    error: str
    detail: str | None = None