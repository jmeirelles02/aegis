# test_step2.py
import asyncio
from src.infrastructure.llm.gemini_client import GeminiClient
from src.core.entities.analysis_request import (
    AnalysisRequest,
    AnalysisType,
    AnalysisDepth,
)
from src.core.entities.analysis_result import SeverityLevel


async def main():
    print("🛡️  Aegis — Testando Passo 2\n")
    print("=" * 60)

    client = GeminiClient()

    # ─────────────────────────────────────────
    # 1. Health Check
    # ─────────────────────────────────────────
    print("\n1️⃣  Health Check do Gemini...")
    is_healthy = await client.health_check()
    status = "✅ Online" if is_healthy else "❌ Offline"
    print(f"   Status: {status}")

    if not is_healthy:
        print("\n⛔ Gemini inacessível. Verifique sua GOOGLE_API_KEY no .env")
        return

    # ─────────────────────────────────────────
    # 2. Análise de Arquitetura + Segurança
    # ─────────────────────────────────────────
    print("\n2️⃣  Executando análise: Arquitetura + Segurança...")
    print("   (pode levar alguns segundos...)\n")

    request = AnalysisRequest(
        title="API REST de E-commerce",
        description="""
        Sistema monolítico em FastAPI com SQLAlchemy.
        Um único banco PostgreSQL para tudo (transacional, analítico e cache).
        Autenticação via JWT com secret hardcoded no código fonte.
        Sem cache, sem filas de mensageria. Deploy em um único servidor VPS.
        Logs apenas com print(). Sem testes automatizados.
        Toda a lógica de negócio dentro dos endpoints do FastAPI.
        Senhas armazenadas em MD5.
        """,
        analysis_types=[AnalysisType.ARCHITECTURE, AnalysisType.SECURITY],
        depth=AnalysisDepth.STANDARD,
        context={
            "language": "Python",
            "team_size": "3",
            "scale": "10k usuarios",
            "deadline": "2 meses",
        },
    )

    result = await client.analyze(request)

    # ─────────────────────────────────────────
    # 3. Exibindo Resultados
    # ─────────────────────────────────────────
    print("=" * 60)
    print(f"📋 RESULTADO: {result.request_title}")
    print(f"🆔 ID: {result.id}")
    print(f"⏱️  Tempo de processamento: {result.processing_time_ms}ms")
    print(f"📊 Score Geral: {result.summary.overall_score}/100")
    print("=" * 60)

    # Summary
    print("\n📝 SUMMARY")
    print(f"   Veredicto: {result.summary.verdict}")
    print(f"   Issues Críticos: {result.summary.critical_issues}")

    print("\n   ✅ Pontos Fortes:")
    for strength in result.summary.strengths:
        print(f"      • {strength}")

    print("\n   ⚡ Quick Wins:")
    for win in result.summary.quick_wins:
        print(f"      • {win}")

    # Findings por severidade
    print("\n" + "=" * 60)
    print("🔍 FINDINGS POR SEVERIDADE")
    print("=" * 60)

    severity_order = [
        SeverityLevel.CRITICAL,
        SeverityLevel.HIGH,
        SeverityLevel.MEDIUM,
        SeverityLevel.LOW,
        SeverityLevel.INFO,
    ]

    severity_icons = {
        SeverityLevel.CRITICAL: "🔴",
        SeverityLevel.HIGH:     "🟠",
        SeverityLevel.MEDIUM:   "🟡",
        SeverityLevel.LOW:      "🔵",
        SeverityLevel.INFO:     "⚪",
    }

    findings_by_severity = result.findings_by_severity

    for severity in severity_order:
        key = severity.value
        findings = findings_by_severity.get(key, [])
        if not findings:
            continue

        icon = severity_icons[severity]
        print(f"\n{icon} {severity.value.upper()} ({len(findings)} findings)")
        print("-" * 40)

        for i, finding in enumerate(findings, 1):
            print(f"\n   [{i}] {finding.title}")
            print(f"   📁 Categoria: {finding.category}")
            print(f"   📄 Descrição: {finding.description}")
            print(f"   💡 Recomendação: {finding.recommendation}")

            if finding.code_example:
                print(f"   💻 Exemplo:")
                for line in finding.code_example.split("\n"):
                    print(f"      {line}")

    # Stats finais
    print("\n" + "=" * 60)
    print("📈 ESTATÍSTICAS")
    print(f"   Total de findings: {len(result.findings)}")
    for severity in severity_order:
        count = len(findings_by_severity.get(severity.value, []))
        if count > 0:
            icon = severity_icons[severity]
            print(f"   {icon} {severity.value.capitalize()}: {count}")

    print(f"\n   Has Critical Issues: {'⚠️  SIM' if result.has_critical_issues else '✅ NÃO'}")
    print("\n" + "=" * 60)
    print("🛡️  Aegis — Passo 2 concluído com sucesso!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())