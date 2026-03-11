ARCHITECTURE_ANALYSIS_PROMPT = """
## Análise de Arquitetura de Software

Analise a seguinte proposta arquitetural e retorne um JSON com este schema exato:

{{
    "findings": [
        {{
            "severity": "critical|high|medium|low|info",
            "category": "string",
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

## Critérios de Avaliação — Arquitetura

Avalie nos seguintes aspectos:
1. **Separação de Responsabilidades** — Camadas bem definidas?
2. **Escalabilidade** — Suporta crescimento horizontal/vertical?
3. **Resiliência** — Pontos únicos de falha? Circuit breakers?
4. **Observabilidade** — Logging, métricas, tracing?
5. **Acoplamento** — Componentes muito acoplados?
6. **Consistência de Dados** — Eventual vs forte? Estratégia clara?
7. **Segurança** — Superfície de ataque? Autenticação/Autorização?

## Proposta para Análise

Título: {title}
Descrição: {description}
Contexto adicional: {context}
Profundidade solicitada: {depth}
"""