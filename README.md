# Aegis (Shadow Architect)

O **Aegis** é uma ferramenta criada para revisar a arquitetura de sistemas. Ele atua como um arquiteto sênior ao seu lado.

Você descreve um sistema. Você escolhe o tipo de análise. O Aegis devolve:
* Uma lista de pontos de atenção com níveis de severidade.
* Recomendações práticas do que fazer a seguir.
* Um resumo executivo com nota, ganhos rápidos e veredicto.

Ele não substitui a revisão humana. A proposta é atuar como um copiloto. Ele levanta riscos e sugere melhorias.

## Para quem é

* Pessoas que desenham sistemas e buscam uma segunda opinião rápida.
* Profissionais que precisam justificar decisões para a equipe e gestão.
* Pessoas que buscam um checklist inteligente de riscos de segurança e performance.
* Profissionais de Engenharia de Software, Engenharia de Dados e Inteligência Artificial.

## O que você consegue analisar

Você pode pedir múltiplas análises simultaneamente:
* **architecture**: camadas, acoplamento, escalabilidade, resiliência, observabilidade.
* **security**: autenticação, OWASP, exposição de dados, rate limit.
* **performance**: gargalos, cache, banco, concorrência, redes.
* **solid**: princípios SOLID e Clean Architecture.
* **data_pipeline**: contratos de dados, idempotência, qualidade, evolução de esquemas.
* **ai_system**: versionamento de modelos, drift, serving, MLOps.

## Como o Aegis funciona

A ferramenta é uma API. Ela orquestra especialistas virtuais. Eles rodam em paralelo.

1) Você envia a descrição do sistema.
2) O Aegis seleciona os tipos de análise solicitados.
3) Ele executa nós especializados simultaneamente.
4) O sistema junta as respostas, remove duplicados e prioriza os itens por severidade.
5) O motor gera um sumário final.

O Aegis divide o problema em partes menores. Isso reduz respostas vagas e aumenta a consistência.

## Como ele foi construído

### 1) Clean Architecture
O projeto foi dividido para facilitar a manutenção e a troca de tecnologias.
* **core/**: regras de negócio.
* **infrastructure/**: implementações reais.
* **api/**: rotas e mapeamento de respostas.

O núcleo do projeto independe do framework web ou do modelo de inteligência artificial.

### 2) Gemini e saída em JSON
O modelo responde em formato JSON. O sistema faz validações defensivas para evitar falhas de formatação.

### 3) LangGraph
O LangGraph orquestra o fluxo de execução. Ele representa o trabalho como um grafo de estado.

### 4) Interface em Streamlit
O Streamlit transforma o código Python em uma página web interativa rapidamente. A interface coleta as entradas do usuário e consome os resultados finais comunicando com a API.
