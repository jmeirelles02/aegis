from pydantic import BaseModel, Field
from datetime import datetime, timezone
from enum import Enum
import uuid

class SeverityLevel(str, Enum):
    """Nível de severidade de um problema encontrado."""
    CRITICAL = "critical"# Blocker — deve ser resolvido
    HIGH     = "high"# Alta prioridade
    MEDIUM   = "medium"# Prioridade média
    LOW      = "low"# Melhoria desejável
    INFO     = "info"# Informativo

class Finding(BaseModel):
    """
    Um problema ou oportunidade encontrado na análise.
    """
    severity: SeverityLevel
    category: str = Field(description="Ex: 'SOLID', 'Performance', 'Security'")
    title: str = Field(description="Título curto do achado")
    description: str = Field(description="Explicação detalhada do problema")
    recommendation: str = Field(description="O que fazer para resolver/melhorar")
    code_example: str | None = Field(
        default=None,
        description="Exemplo de código ilustrando a solução (opcional)",
    )

class AnalysisSummary(BaseModel):
    """Resumo executivo da análise."""
    overall_score: int = Field(ge=0, le=100, description="Score geral de 0 a 100")
    strengths: list[str] = Field(description="Pontos fortes da arquitetura")
    critical_issues: int = Field(description="Quantidade de issues críticos")
    quick_wins: list[str] = Field(description="Melhorias rápidas de alto impacto")
    verdict: str = Field(description="Veredicto final do Shadow Architect")

class AnalysisResult(BaseModel):
    """
    Resultado completo de uma análise do Aegis.
    Entidade imutável — representa um resultado já processado.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    request_title: str
    analysis_types: list[str]
    findings: list[Finding] = Field(default_factory=list)
    summary: AnalysisSummary
    raw_response: str = Field(description="Resposta bruta do LLM para debug")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    processing_time_ms: int = Field(description="Tempo de processamento em ms")

    @property
    def has_critical_issues(self) -> bool:
        return any(f.severity == SeverityLevel.CRITICAL for f in self.findings)

    @property
    def findings_by_severity(self) -> dict[str, list[Finding]]:
        result: dict[str, list[Finding]] = {}
        for finding in self.findings:
            key = finding.severity.value
            result.setdefault(key, []).append(finding)
        return result   