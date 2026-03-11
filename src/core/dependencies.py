from functools import lru_cache
from src.core.interfaces.llm_gateway import LLMGateway
from src.core.interfaces.analysis_repository import AnalysisRepository
from src.infrastructure.llm.langgraph_gateway import LangGraphGateway
from src.infrastructure.repositories.in_memory_repository import InMemoryAnalysisRepository
from src.core.use_cases.analyze_architecture import AnalyzeArchitectureUseCase
from src.core.use_cases.get_analysis import GetAnalysisUseCase
from src.core.use_cases.list_analyses import ListAnalysesUseCase


@lru_cache(maxsize=1)
def get_llm_gateway() -> LLMGateway:
    return LangGraphGateway()


@lru_cache(maxsize=1)
def get_repository() -> AnalysisRepository:
    return InMemoryAnalysisRepository()


def get_analyze_use_case() -> AnalyzeArchitectureUseCase:
    return AnalyzeArchitectureUseCase(
        llm_gateway=get_llm_gateway(),
        repository=get_repository(),
    )


def get_get_analysis_use_case() -> GetAnalysisUseCase:
    return GetAnalysisUseCase(repository=get_repository())


def get_list_analyses_use_case() -> ListAnalysesUseCase:
    return ListAnalysesUseCase(repository=get_repository())