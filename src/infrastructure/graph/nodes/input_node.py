import logging
from src.infrastructure.graph.state import AegisState

logger = logging.getLogger(__name__)


async def input_node(state: AegisState) -> dict:
    """
    Nó de entrada: valida e prepara o estado inicial.
    """
    logger.info(f"[input_node] Iniciando análise: {state['request'].title}")

    active_types = [t.value for t in state["request"].analysis_types]

    return {
        "active_analysis_types": active_types,
        "current_step": "routing",
        "errors": [],
        "raw_findings": [],
        "findings": [],
        "summary": None,
        "processing_time_ms": 0,
    }