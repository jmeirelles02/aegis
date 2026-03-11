import traceback

try:
    from src.infrastructure.graph.state import AegisState
    print("✅ state OK")
except Exception as e:
    print(f"❌ state: {e}")
    traceback.print_exc()

try:
    from src.infrastructure.graph.nodes.input_node import input_node
    print("✅ input_node OK")
except Exception as e:
    print(f"❌ input_node: {e}")
    traceback.print_exc()

try:
    from src.infrastructure.graph.nodes.routing_node import routing_node, route_to_analyzers
    print("✅ routing_node OK")
except Exception as e:
    print(f"❌ routing_node: {e}")
    traceback.print_exc()

try:
    from src.infrastructure.graph.nodes.analyzer_nodes import architecture_node
    print("✅ analyzer_nodes OK")
except Exception as e:
    print(f"❌ analyzer_nodes: {e}")
    traceback.print_exc()

try:
    from src.infrastructure.graph.nodes.aggregator_node import aggregator_node
    print("✅ aggregator_node OK")
except Exception as e:
    print(f"❌ aggregator_node: {e}")
    traceback.print_exc()

try:
    from src.infrastructure.graph.nodes.summary_node import summary_node
    print("✅ summary_node OK")
except Exception as e:
    print(f"❌ summary_node: {e}")
    traceback.print_exc()

try:
    from langgraph.graph import StateGraph, START, END
    print("✅ langgraph OK")
except Exception as e:
    print(f"❌ langgraph: {e}")
    traceback.print_exc()

try:
    from src.infrastructure.graph.aegis_graph import build_aegis_graph
    print("✅ build_aegis_graph importado OK")
    graph = build_aegis_graph()
    print("✅ grafo compilado OK")
except Exception as e:
    print(f"❌ aegis_graph: {e}")
    traceback.print_exc()