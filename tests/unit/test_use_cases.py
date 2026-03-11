import pytest
from unittest.mock import AsyncMock
from src.core.use_cases.analyze_architecture import AnalyzeArchitectureUseCase
from src.core.use_cases.get_analysis import GetAnalysisUseCase
from src.core.use_cases.list_analyses import ListAnalysesUseCase
from src.core.entities.analysis_request import AnalysisRequest, AnalysisType

class TestAnalyzeArchitectureUseCase:

    @pytest.mark.asyncio
    async def test_execute_success(
        self,
        mock_llm_gateway,
        mock_repository,
        sample_request,
        sample_result,
    ):
        use_case = AnalyzeArchitectureUseCase(
            llm_gateway=mock_llm_gateway,
            repository=mock_repository,
        )
        result = await use_case.execute(sample_request)

        assert result == sample_result
        mock_llm_gateway.analyze.assert_called_once_with(sample_request)
        mock_repository.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_validate_short_description(
        self,
        mock_llm_gateway,
        mock_repository,
    ):
        use_case = AnalyzeArchitectureUseCase(
            llm_gateway=mock_llm_gateway,
            repository=mock_repository,
        )
        bad_request = AnalysisRequest(
            title="Teste",
            description="Sistema monolítico com banco de dados único.",
        )
        bad_request.__dict__["description"] = "muito curta aqui"

        with pytest.raises(ValueError, match="muito curta"):
            await use_case.execute(bad_request)

    @pytest.mark.asyncio
    async def test_llm_gateway_called_once(
        self,
        mock_llm_gateway,
        mock_repository,
        sample_request,
    ):
        use_case = AnalyzeArchitectureUseCase(
            llm_gateway=mock_llm_gateway,
            repository=mock_repository,
        )
        await use_case.execute(sample_request)
        assert mock_llm_gateway.analyze.call_count == 1

class TestGetAnalysisUseCase:

    @pytest.mark.asyncio
    async def test_execute_found(self, mock_repository, sample_result):
        use_case = GetAnalysisUseCase(repository=mock_repository)
        result = await use_case.execute(sample_result.id)
        assert result == sample_result

    @pytest.mark.asyncio
    async def test_execute_not_found(self, mock_repository):
        mock_repository.find_by_id.return_value = None
        use_case = GetAnalysisUseCase(repository=mock_repository)

        with pytest.raises(ValueError, match="não encontrada"):
            await use_case.execute("id-invalido")

    @pytest.mark.asyncio
    async def test_execute_empty_id(self, mock_repository):
        use_case = GetAnalysisUseCase(repository=mock_repository)

        with pytest.raises(ValueError, match="não pode estar vazio"):
            await use_case.execute("")

class TestListAnalysesUseCase:

    @pytest.mark.asyncio
    async def test_execute_returns_list(self, mock_repository, sample_result):
        use_case = ListAnalysesUseCase(repository=mock_repository)
        results = await use_case.execute()

        assert isinstance(results, list)
        assert len(results) == 1
        assert results[0] == sample_result

    @pytest.mark.asyncio
    async def test_execute_empty_list(self, mock_repository):
        mock_repository.list_all.return_value = []
        use_case = ListAnalysesUseCase(repository=mock_repository)
        results = await use_case.execute()
        assert results == []