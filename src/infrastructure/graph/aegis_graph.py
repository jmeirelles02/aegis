import logging
from langgraph.graph import StateGraph, START, END

from src.infrastructure.graph.state import AegisState
from src.infrastructure.graph.nodes.input_node import input_node
from src.infrastructure.graph.nodes.routing_node import routing_node, route_to_analyzers
from src.infrastructure.graph.nodes.analyzer_nodes import (
    architecture_node,
    solid_node,
    performance_node,
    security_node,
    data_pipeline_node,
    ai_system_node,
)
from src.infrastructure.graph.nodes.aggregator_node import aggregator_node
from src.infrastructure.graph.nodes.summary_node import summary_node

logger = logging.getLogger(__name__)

_aegis_graph = None


def build_aegis_graph():
    """Constrói e compila o grafo do Aegis."""
    graph = StateGraph(AegisState)

    graph.add_node("input_node",         input_node)
    graph.add_node("routing_node",       routing_node)
    graph.add_node("architecture_node",  architecture_node)
    graph.add_node("solid_node",         solid_node)
    graph.add_node("performance_node",   performance_node)
    graph.add_node("security_node",      security_node)
    graph.add_node("data_pipeline_node", data_pipeline_node)
    graph.add_node("ai_system_node",     ai_system_node)
    graph.add_node("aggregator_node",    aggregator_node)
    graph.add_node("summary_node",       summary_node)

    graph.add_edge(START,        "input_node")
    graph.add_edge("input_node", "routing_node")

    graph.add_conditional_edges(
        "routing_node",
        route_to_analyzers,
        {
            "architecture_node":  "architecture_node",
            "solid_node":         "solid_node",
            "performance_node":   "performance_node",
            "security_node":      "security_node",
            "data_pipeline_node": "data_pipeline_node",
            "ai_system_node":     "ai_system_node",
        },
    )

    for node in [
        "architecture_node",
        "solid_node",
        "performance_node",
        "security_node",
        "data_pipeline_node",
        "ai_system_node",
    ]:
        graph.add_edge(node, "aggregator_node")

    graph.add_edge("aggregator_node", "summary_node")
    graph.add_edge("summary_node",    END)

    compiled = graph.compile()
    logger.info("✅ Aegis graph compilado com sucesso")
    return compiled


def get_aegis_graph():
    """
    Retorna o grafo compilado (singleton).
    Lazy initialization — compila apenas na primeira chamada.
    """
    global _aegis_graph
    if _aegis_graph is None:
        logger.info("Compilando Aegis graph...")
        _aegis_graph = build_aegis_graph()
    return _aegis_graph


aegis_graph = get_aegis_graph()