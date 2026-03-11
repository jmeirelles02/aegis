DATA_PIPELINE_PROMPT = """
## Análise de Pipeline de Dados

Analise o fluxo de dados proposto e retorne um JSON com este schema exato:

{{
    "findings": [
        {{
            "severity": "critical|high|medium|low|info",
            "category": "string (ex: Ingestion, Transform, Storage, Lineage)",
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

## Aspectos de Data Pipeline a Analisar

1. **Idempotência** — Reprocessamento seguro?
2. **Schema Evolution** — Mudanças de schema sem downtime?
3. **Data Quality** — Validação e contratos de dados?
4. **Backpressure** — Controle de fluxo entre producers/consumers?
5. **Observabilidade** — Lineage, data quality metrics, SLAs?
6. **Late Arriving Data** — Estratégia para dados atrasados?
7. **Storage Strategy** — Hot/Warm/Cold? Particionamento?

## Proposta para Análise

Título: {title}
Descrição: {description}
Contexto adicional: {context}
Profundidade solicitada: {depth}
"""