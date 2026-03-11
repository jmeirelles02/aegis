# src/infrastructure/llm/prompts/ai_system.py

AI_SYSTEM_PROMPT = """
## Análise de Sistema de IA/ML

Analise a arquitetura do sistema de IA e retorne um JSON com este schema exato:

{{
    "findings": [
        {{
            "severity": "critical|high|medium|low|info",
            "category": "string (ex: MLOps, Model Serving, Data Drift, Monitoring)",
            "title": "string",
            "description": "string detalhada",
            "recommendation": "string acionável",
            "code_example": "string com código ou null"
        }}
    ],
    "summary": {{
        "overall_score": 0-100,
        "strengths": ["string"],
        "critical_issues": 0,
        "quick_wins": ["string"],
        "verdict": "string do veredicto final"
    }}
}}

## Aspectos de AI/ML a Analisar

1. **Model Serving** — Latência de inferência? Batching?
2. **Feature Store** — Consistência entre treino e serving?
3. **Data Drift** — Monitoramento de distribuição?
4. **Model Versioning** — Rollback possível?
5. **Feedback Loop** — Coleta de dados para retreino?
6. **Explainability** — Decisões auditáveis?
7. **Fairness & Bias** — Avaliação de viés nos dados/modelo?

## Proposta para Análise

Título: {title}
Descrição: {description}
Contexto adicional: {context}
Profundidade solicitada: {depth}
"""