import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from httpx import AsyncClient, ASGITransport

from src.core.entities.analysis_request import AnalysisRequest, AnalysisType
from src.core.entities.analysis_result import (
    AnalysisResult,
    Finding,
    AnalysisSummary,
    SeverityLevel,
)

@pytest.fixture
def sample_finding() -> Finding:
    return Finding(
        severity=SeverityLevel.CRITICAL,
        category="Architecture",
        title="Ponto único de falha",
        description="O sistema não possui redundância nos componentes críticos.",
        recommendation="Implemente redundância e circuit breakers nos serviços principais.",
    )

@pytest.fixture
def sample_summary() -> AnalysisSummary:
    return AnalysisSummary(
        overall_score=62,
        strengths=["Simplicidade", "Baixa latência interna"],
        critical_issues=1,
        quick_wins=["Adicionar cache Redis", "Configurar health checks"],
        verdict="Arquitetura funcional mas com riscos significativos de escalabilidade.",
    )

@pytest.fixture
def sample_result(sample_finding, sample_summary) -> AnalysisResult:
    return AnalysisResult(
        request_title="Sistema de Teste",
        analysis_types=["architecture"],
        findings=[sample_finding],
        summary=sample_summary,
        raw_response="{}",
        processing_time_ms=500,
    )

@pytest.fixture
def sample_request() -> AnalysisRequest:
    return AnalysisRequest(
        title="Sistema de Teste",
        description="Monolito FastAPI com PostgreSQL e sem cache nem filas de mensageria.",
        analysis_types=[AnalysisType.ARCHITECTURE],
    )

@pytest.fixture
def mock_repository(sample_result) -> MagicMock:
    repo = MagicMock()
    repo.save = AsyncMock(return_value=sample_result)
    repo.find_by_id = AsyncMock(return_value=sample_result)
    repo.list_all = AsyncMock(return_value=[sample_result])
    return repo

@pytest.fixture
def mock_llm_gateway(sample_result) -> MagicMock:
    gateway = MagicMock()
    gateway.analyze = AsyncMock(return_value=sample_result)
    return gateway

@pytest.fixture
async def client(mock_repository, mock_llm_gateway, sample_result) -> AsyncClient:
    """
    AsyncClient com use cases reais instanciados com mocks injetados,
    patcheando as funções de fábrica nas rotas para retornar os use cases mockados.

    Ao usar use cases reais (com mocks injetados), qualquer alteração no
    mock_repository feita pelo teste se reflete automaticamente no comportamento
    do use case durante a request.
    """
    from src.core.use_cases.analyze_architecture import AnalyzeArchitectureUseCase
    from src.core.use_cases.get_analysis import GetAnalysisUseCase
    from src.core.use_cases.list_analyses import ListAnalysesUseCase

    analyze_uc = AnalyzeArchitectureUseCase(
        llm_gateway=mock_llm_gateway,
        repository=mock_repository,
    )
    get_uc = GetAnalysisUseCase(repository=mock_repository)
    list_uc = ListAnalysesUseCase(repository=mock_repository)

    with (
        patch("src.api.routes.analysis.get_analyze_use_case", return_value=analyze_uc),
        patch("src.api.routes.analysis.get_get_analysis_use_case", return_value=get_uc),
        patch("src.api.routes.analysis.get_list_analyses_use_case", return_value=list_uc),
    ):
        from src.api.app import create_app
        app = create_app()

        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
        ) as ac:
            yield ac
