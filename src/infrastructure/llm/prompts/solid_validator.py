# src/infrastructure/llm/prompts/solid_validator.py

SOLID_ANALYSIS_PROMPT = """
## Validação de Princípios SOLID e Clean Architecture

Analise o design proposto e retorne um JSON com este schema exato:

{{
    "findings": [
        {{
            "severity": "critical|high|medium|low|info",
            "category": "string (ex: SRP, OCP, DIP, Clean Architecture)",
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

## Princípios a Verificar

### SOLID
- **S** — Single Responsibility: cada módulo tem uma razão para mudar?
- **O** — Open/Closed: extensível sem modificação?
- **L** — Liskov Substitution: subtipos substituíveis?
- **I** — Interface Segregation: interfaces coesas e específicas?
- **D** — Dependency Inversion: depende de abstrações?

### Clean Architecture
- Direção das dependências (inward only?)
- Isolamento do domínio de frameworks
- Testabilidade das camadas
- Use Cases bem definidos?

## Proposta para Análise

Título: {title}
Descrição: {description}
Contexto adicional: {context}
Profundidade solicitada: {depth}
"""