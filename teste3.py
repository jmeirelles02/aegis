# test_step3.py
import asyncio
import time
import logging

logging.basicConfig(level=logging.INFO)

from src.infrastructure.graph.aegis_graph import aegis_graph
from src.core.entities.analysis_request import (
    AnalysisRequest,
    AnalysisType,
    AnalysisDepth,
)
from src.core.entities.analysis_result import SeverityLevel


async def main():
    print("🛡️  Aegis — Testando Passo 3: LangGraph\n")
    print("=" * 60)

    request = AnalysisRequest(
        title="Plataforma de Streaming de Dados com ML",
        description="""
        Sistema com Kafka para ingestão de eventos em tempo real.
        Spark Structured Streaming para processamento.
        Modelo de detecção de fraude servido via FastAPI.
        Feature store customizado em Redis.
        Sem versionamento de modelos. Sem monitoramento de data drift.
        Schema do Kafka não gerenciado (sem Schema Registry).
        """,
        analysis_types=[
            AnalysisType.ARCHITECTURE,
            AnalysisType.DATA_PIPELINE,
            AnalysisType.AI_SYSTEM,
        ],
        depth=AnalysisDepth.STANDARD,
        context={
            "language": "Python",
            "scale": "1M eventos/hora",
            "latency": "< 200ms p99",
        },
    )

    # Estado inicial
    initial_state: dict = {"request": request}

    print(f"📋 Analisando: {request.title}")
    print(f"🔍 Tipos: {[t.value for t in request.analysis_types]}")
    print("\n⏳ Executando grafo...\n")

    start = time.monotonic()
    final_state = await aegis_graph.ainvoke(initial_state)
    elapsed = int((time.monotonic() - start) * 1000)

    # ── Resultados ──────────────────────────────────────────────
    findings = final_state.get("findings", [])
    summary  = final_state.get("summary")

    print("=" * 60)
    print(f"⏱️  Tempo total: {elapsed}ms")
    print(f"📊 Score: {summary.overall_score}/100")
    print(f"🔍 Total de findings: {len(findings)}")
    print(f"📌 Step final: {final_state.get('current_step')}")

    # Erros durante o pipeline
    errors = final_state.get("errors", [])
    if errors:
        print(f"\n⚠️  Erros no pipeline:")
        for err in errors:
            print(f"   • {err}")

    # Summary
    print(f"\n📝 Veredicto: {summary.verdict}")

    print("\n✅ Pontos Fortes:")
    for s in summary.strengths:
        print(f"   • {s}")

    print("\n⚡ Quick Wins:")
    for q in summary.quick_wins:
        print(f"   • {q}")

    # Findings por severidade
    severity_icons = {
        SeverityLevel.CRITICAL: "🔴",
        SeverityLevel.HIGH:     "🟠",
        SeverityLevel.MEDIUM:   "🟡",
        SeverityLevel.LOW:      "🔵",
        SeverityLevel.INFO:     "⚪",
    }

    print("\n" + "=" * 60)
    print("🔍 FINDINGS")
    print("=" * 60)

    for finding in findings:
        icon = severity_icons.get(finding.severity, "⚪")
        print(f"\n{icon} [{finding.severity.value.upper()}] {finding.title}")
        print(f"   📁 {finding.category}")
        print(f"   📄 {finding.description[:120]}...")
        print(f"   💡 {finding.recommendation[:120]}...")

    print("\n" + "=" * 60)
    print("🛡️  Aegis — Passo 3 concluído com sucesso!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())