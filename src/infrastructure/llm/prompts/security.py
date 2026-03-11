# src/infrastructure/llm/prompts/security.py

SECURITY_ANALYSIS_PROMPT = """
## Análise de Segurança

Analise a superfície de ataque e retorne um JSON com este schema exato:

{{
    "findings": [
        {{
            "severity": "critical|high|medium|low|info",
            "category": "string (ex: Auth, Injection, Data Exposure, OWASP)",
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

## Aspectos de Segurança a Analisar

1. **Autenticação/Autorização** — JWT? OAuth2? RBAC?
2. **Exposição de Dados** — Dados sensíveis em logs/responses?
3. **Injection** — SQL, Command, SSRF?
4. **Secrets Management** — Credenciais hardcoded?
5. **TLS/Criptografia** — Dados em trânsito e em repouso?
6. **Rate Limiting** — Proteção contra abuso?
7. **Dependências** — Bibliotecas desatualizadas/vulneráveis?

## Proposta para Análise

Título: {title}
Descrição: {description}
Contexto adicional: {context}
Profundidade solicitada: {depth}
"""