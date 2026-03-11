# test_sanity.py
from src.config.settings import settings
from src.core.entities.analysis_request import AnalysisRequest, AnalysisType
from src.core.entities.analysis_result import AnalysisResult, Finding, AnalysisSummary, SeverityLevel

def test_settings():
    print(f"✅ App: {settings.app_name}")
    print(f"✅ Env: {settings.app_env}")
    print(f"✅ Model: {settings.gemini_model}")

def test_entities():
    req = AnalysisRequest(
        title="Teste de Arquitetura",
        description="Sistema distribuído com event sourcing e CQRS para alta disponibilidade.",
        analysis_types=[AnalysisType.ARCHITECTURE, AnalysisType.SOLID],
    )
    print(f"✅ Request criada: {req.title}")
    print(f"✅ Tipos: {[t.value for t in req.analysis_types]}")

if __name__ == "__main__":
    test_settings()
    test_entities()
    print("\n🛡️ Aegis — Passo 1 concluído com sucesso!")