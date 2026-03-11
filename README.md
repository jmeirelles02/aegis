# Aegis (Shadow Architect)

O **Aegis** é uma ferramenta que eu criei para fazer uma coisa bem específica: **ajudar a pensar arquitetura** como se você tivesse um(a) arquiteto(a) sênior ao seu lado revisando suas ideias.

Você descreve um sistema (ou uma decisão técnica), escolhe que tipo de análise quer (arquitetura, segurança, performance, dados, IA etc.) e o Aegis devolve:

- uma lista de **pontos de atenção** (com severidade: crítico/alto/médio/baixo),
- **recomendações práticas** do que fazer a seguir,
- e um **resumo executivo** com “nota”, quick wins e veredicto.

Ele não substitui revisão humana — a proposta é ser um **copiloto**: levantar riscos, sugerir melhorias e acelerar o ciclo “escrever → revisar → ajustar”.

---

## Para quem é

- Quem está desenhando um sistema e quer uma segunda opinião rápida.
- Quem precisa justificar decisões (trade-offs) para time/gestão.
- Quem quer um checklist “inteligente” de riscos de segurança/performance.
- Quem trabalha com **Engenharia de Software**, **Engenharia de Dados** e/ou **IA/MLOps**.

---

## O que você consegue analisar com ele

Você pode pedir uma ou várias análises ao mesmo tempo:

- **architecture**: camadas, acoplamento, escalabilidade, resiliência, observabilidade
- **security**: autenticação, secrets, OWASP, exposição de dados, rate limit
- **performance**: gargalos, cache, banco, concorrência, redes
- **solid**: princípios SOLID e Clean Architecture (mais “design”)
- **data_pipeline**: contratos de dados, idempotência, qualidade, schema evolution
- **ai_system**: versionamento de modelos, drift, serving, MLOps

---

## Como o Aegis funciona por dentro (sem enrolação)

Por trás, o Aegis é uma API que orquestra “especialistas” (nós) que rodam em paralelo.

1) **Você manda uma descrição do seu sistema**  
2) O Aegis escolhe quais análises executar (ex.: arquitetura + segurança)  
3) Ele roda **nós especializados em paralelo** (um nó por tipo de análise)  
4) Junta tudo, **remove duplicados**, prioriza por severidade  
5) Gera um **sumário final** (nota, quick wins e veredicto)

O ponto importante: em vez de “uma chamada gigante ao LLM”, o Aegis separa o problema em partes, porque isso tende a:
- reduzir respostas vagas,
- aumentar consistência,
- e permitir evoluir o sistema (adicionar novos nós no futuro).

---

## Como ele foi construído (decisões que guiaram o projeto)

### 1) Clean Architecture (de verdade)
O projeto foi dividido para ficar fácil de manter e trocar peças:

- **core/**: regras do negócio (entidades, casos de uso, interfaces)
- **infrastructure/**: implementações reais (LangGraph, Gemini, repositório)
- **api/**: FastAPI (rotas, schemas e mapeamento de resposta)

A ideia aqui é: **o coração do projeto não depende do FastAPI nem do Gemini**.  
Se amanhã você quiser trocar o modelo, ou persistir em Postgres, o core não muda.

### 2) Gemini + saída em JSON
O Aegis pede que o modelo responda **sempre em JSON** (findings + summary).  
Na prática, LLM às vezes “escapa” do formato, então há parsing defensivo:
- remove ```json fences
- lida com respostas multimodais do Gemini (lista de chunks `type=text`)
- tem fallback para não quebrar tudo quando o JSON vem torto

### 3) LangGraph para orquestrar o fluxo
O LangGraph foi escolhido porque ele representa bem o que o Aegis faz:
um **workflow com estado**, nós paralelos e um passo de consolidação.

---

## Como rodar localmente

### Pré-requisitos
- Python 3.11+ (recomendado 3.11/3.12)
- Uma API Key do Gemini

### 1) Ambiente virtual
**Windows (PowerShell):**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux/macOS:**
```bash
python -m venv .venv
source .venv/bin/activate
```

### 2) Instalar dependências
Se você está usando `pyproject.toml`:
```bash
pip install -e ".[dev]"
```

### 3) Criar `.env`
Crie um arquivo `.env` na raiz:

```env
GOOGLE_API_KEY=coloque_sua_api_key_aqui
GEMINI_MODEL=escolha-seu-modelo

APP_ENV=development
APP_DEBUG=true
APP_HOST=0.0.0.0
APP_PORT=8000

LLM_TEMPERATURE=0.3
LLM_MAX_TOKENS=8192
```


### 4) Subir o servidor
```bash
python main.py
```

Abra:
- Swagger: `http://localhost:8000/docs`

---

## Como usar (exemplo simples)

No Swagger, use `POST /analyses/` e mande algo como:

```json
{
  "title": "API de E-commerce",
  "description": "Monolito FastAPI com PostgreSQL único para tudo, sem cache, sem filas. JWT hardcoded. Senhas em MD5. Logs com print(). Sem testes.",
  "analysis_types": ["architecture", "security"],
  "depth": "standard",
  "context": {"language": "Python", "scale": "10k users"}
}
```

Você vai receber:
- achados priorizados (crítico → baixo),
- recomendações,
- e um sumário (score, quick wins, veredicto).

---

## Estrutura do projeto (guia rápido)

- `src/api/` — FastAPI (rotas, schemas, app)
- `src/core/` — domínio + casos de uso + interfaces
- `src/infrastructure/graph/` — LangGraph (nós e estado)
- `src/infrastructure/llm/` — gateway do LLM + prompts
- `src/infrastructure/repositories/` — repositório (MVP: in-memory)

---

## Limitações atuais (honesto e direto)
- Persistência é **in-memory** (reiniciou o servidor, perdeu histórico).
- A qualidade da resposta depende do quão bem você descreve o sistema.
- LLM pode repetir achados parecidos (mitigado com deduplicação, mas não perfeito).
- Sem autenticação/rate limit ainda (não é ideal para expor publicamente do jeito que está).

---

## Próximos passos (ideias de evolução)
- Persistência real (PostgreSQL/MongoDB)
- Autenticação (API key) + rate limiting
- Observabilidade (logs estruturados + métricas)
- Proteções contra prompt injection
- Mais nós (ex.: “Reviewer Node” para revisar a própria resposta antes de retornar)

