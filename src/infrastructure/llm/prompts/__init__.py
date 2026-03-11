from src.core.entities.analysis_request import AnalysisType
from .architect import ARCHITECTURE_ANALYSIS_PROMPT
from .solid_validator import SOLID_ANALYSIS_PROMPT
from .performance import PERFORMANCE_ANALYSIS_PROMPT
from .security import SECURITY_ANALYSIS_PROMPT
from .data_pipeline import DATA_PIPELINE_PROMPT
from .ai_system import AI_SYSTEM_PROMPT

PROMPT_REGISTRY: dict[AnalysisType, str] = {
    AnalysisType.ARCHITECTURE:  ARCHITECTURE_ANALYSIS_PROMPT,
    AnalysisType.SOLID:         SOLID_ANALYSIS_PROMPT,
    AnalysisType.PERFORMANCE:   PERFORMANCE_ANALYSIS_PROMPT,
    AnalysisType.SECURITY:      SECURITY_ANALYSIS_PROMPT,
    AnalysisType.DATA_PIPELINE: DATA_PIPELINE_PROMPT,
    AnalysisType.AI_SYSTEM:     AI_SYSTEM_PROMPT,
}

__all__ = ["PROMPT_REGISTRY"]