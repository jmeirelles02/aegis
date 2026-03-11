# src/core/entities/analysis_request.py

from pydantic import BaseModel, Field
from enum import Enum


class AnalysisType(str, Enum):
    """Tipos de análise que o Aegis suporta."""
    ARCHITECTURE   = "architecture"    # Análise geral de arquitetura
    SOLID          = "solid"           # Validação de princípios SOLID
    PERFORMANCE    = "performance"     # Gargalos e otimizações
    SECURITY       = "security"        # Vulnerabilidades e boas práticas
    DATA_PIPELINE  = "data_pipeline"   # Fluxos de dados (Eng. de Dados)
    AI_SYSTEM      = "ai_system"       # Sistemas de IA/ML


class AnalysisDepth(str, Enum):
    """Profundidade da análise."""
    QUICK    = "quick"       # Revisão rápida (~30s)
    STANDARD = "standard"   # Análise padrão (~1min)
    DEEP     = "deep"        # Análise profunda (~2min)


class AnalysisRequest(BaseModel):
    """
    Entidade que representa uma solicitação de análise ao Aegis.
    Princípio SRP: responsável apenas por representar a requisição.
    """
    title: str = Field(
        ...,
        min_length=3,
        max_length=200,
        description="Título descritivo da proposta/sistema",
        examples=["API de Pagamentos com Microserviços"],
    )
    description: str = Field(
        ...,
        min_length=20,
        max_length=10_000,
        description="Descrição detalhada da arquitetura ou decisão de design",
    )
    analysis_types: list[AnalysisType] = Field(
        default=[AnalysisType.ARCHITECTURE],
        min_length=1,
        description="Tipos de análise desejados",
    )
    depth: AnalysisDepth = Field(
        default=AnalysisDepth.STANDARD,
        description="Profundidade da análise",
    )
    context: dict[str, str] = Field(
        default_factory=dict,
        description="Contexto adicional: linguagem, stack, restrições, etc.",
        examples=[{"language": "Python", "team_size": "5", "scale": "1M req/day"}],
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Sistema de Recomendação em Tempo Real",
                "description": "Arquitetura com Kafka para ingestão, "
                               "Redis para cache e modelo ML servido via FastAPI.",
                "analysis_types": ["architecture", "performance", "ai_system"],
                "depth": "deep",
                "context": {
                    "language": "Python",
                    "scale": "500k usuarios ativos",
                    "latency_requirement": "< 100ms",
                },
            }
        }
    }