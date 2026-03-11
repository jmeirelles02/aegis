import logging
from src.infrastructure.graph.state import AegisState
from src.core.entities.analysis_request import AnalysisType

logger = logging.getLogger(__name__)


async def routing_node(state: AegisState) -> dict:
    """
    Nó de roteamento: decide quais agentes de análise serão acionados.
    Não executa análise — apenas prepara o roteamento.
    """
    active = state["active_analysis_types"]
    logger.info(f"[routing_node] Roteando para: {active}")

    return {
        "current_step": "analyzing",
    }


def route_to_analyzers(state: AegisState) -> list[str]:
    """
    Função de roteamento condicional do LangGraph.
    Retorna a lista de nós que devem ser executados em paralelo.
    """
    type_to_node = {
        AnalysisType.ARCHITECTURE.value:  "architecture_node",
        AnalysisType.SOLID.value:         "solid_node",
        AnalysisType.PERFORMANCE.value:   "performance_node",
        AnalysisType.SECURITY.value:      "security_node",
        AnalysisType.DATA_PIPELINE.value: "data_pipeline_node",
        AnalysisType.AI_SYSTEM.value:     "ai_system_node",
    }

    active = state["active_analysis_types"]
    nodes = [type_to_node[t] for t in active if t in type_to_node]

    logger.info(f"[route_to_analyzers] Nós ativos: {nodes}")
    return nodes