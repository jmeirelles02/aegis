# test_step4.py
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

from src.core.dependencies import (
    get_analyze_use_case,
    get_get_analysis_use_case,
    get_list_analyses_use_case,
)
from src.core.entities.analysis_request import (
    AnalysisRequest,
    AnalysisType,
    AnalysisDepth,
)


async def main():
    print("🛡️  Aegis — Testando Passo 4: Use Cases\n")
    print("=" * 60)

    # ── 1. Analyze ──────────────────────────────────────────────
    print("\n1️⃣  Executando AnalyzeArchitectureUseCase...")

    analyze = get_analyze_use_case()

    request = AnalysisRequest(
        title="Microserviço de Autenticação",
        description="""
        Serviço de autenticação com JWT usando FastAPI.
        Banco PostgreSQL compartilhado com outros serviços.
        Sem refresh tokens. Tokens com expiração de 30 dias.
        Sem rate limiting no endpoint de login.
        Logs com dados sensíveis (email, IP).
        Deploy via Docker sem secrets manager.
        """,
        analysis_types=[AnalysisType.SECURITY, AnalysisType.ARCHITECTURE],
        depth=AnalysisDepth.STANDARD,
        context={"language": "Python", "scale": "50k users"},
    )

    result = await analyze.execute(request)

    print(f"   ✅ Análise concluída!")
    print(f"   🆔 ID: {result.id}")
    print(f"   📊 Score: {result.summary.overall_score}/100")
    print(f"   🔍 Findings: {len(result.findings)}")
    print(f"   ⚠️  Críticos: {result.summary.critical_issues}")
    print(f"   📝 Veredicto: {result.summary.verdict[:100]}...")

    # ── 2. Get by ID ────────────────────────────────────────────
    print(f"\n2️⃣  Executando GetAnalysisUseCase...")

    get_uc = get_get_analysis_use_case()
    found = await get_uc.execute(result.id)

    print(f"   ✅ Encontrado: {found.request_title}")
    print(f"   🕐 Criado em: {found.created_at}")

    # ── 3. List All ─────────────────────────────────────────────
    print(f"\n3️⃣  Executando ListAnalysesUseCase...")

    list_uc = get_list_analyses_use_case()
    all_results = await list_uc.execute()

    print(f"   ✅ Total de análises: {len(all_results)}")

    # ── 4. Validação de negócio ─────────────────────────────────
    print(f"\n4️⃣  Testando validações de negócio...")

    try:
        bad_request = AnalysisRequest(
            title="Teste",
            description="curta",  # muito curta
            analysis_types=[AnalysisType.ARCHITECTURE],
        )
        await analyze.execute(bad_request)
        print("   ❌ Deveria ter lançado ValueError!")
    except ValueError as e:
        print(f"   ✅ Validação funcionou: {e}")

    # ── 5. Not Found ────────────────────────────────────────────
    print(f"\n5️⃣  Testando ID inexistente...")

    try:
        await get_uc.execute("id-que-nao-existe")
        print("   ❌ Deveria ter lançado ValueError!")
    except ValueError as e:
        print(f"   ✅ Not found funcionou: {e}")

    print("\n" + "=" * 60)
    print("🛡️  Aegis — Passo 4 concluído com sucesso!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())