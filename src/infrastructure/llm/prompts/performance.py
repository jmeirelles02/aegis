PERFORMANCE_ANALYSIS_PROMPT = """
## Análise de Performance e Escalabilidade

Analise os potenciais gargalos e retorne um JSON com este schema exato:

{{
    "findings": [
        {{
            "severity": "critical|high|medium|low|info",
            "category": "string (ex: Caching, Database, Network, Concurrency)",
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

## Aspectos de Performance a Analisar

1. **Latência** — Pontos de latência oculta? N+1 queries?
2. **Throughput** — Capacidade de processar volume esperado?
3. **Caching** — Estratégia de cache? Invalidação?
4. **Concorrência** — Race conditions? Deadlocks potenciais?
5. **I/O Bound vs CPU Bound** — Estratégia adequada (async/threads)?
6. **Banco de Dados** — Índices? Queries N+1? Connection pooling?
7. **Rede** — Chattiness? Payload size? Compressão?

## Proposta para Análise

Título: {title}
Descrição: {description}
Contexto adicional: {context}
Profundidade solicitada: {depth}
"""