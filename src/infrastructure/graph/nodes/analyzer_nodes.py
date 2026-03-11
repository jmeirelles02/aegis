import json
import logging
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

from src.infrastructure.graph.state import AegisState
from src.infrastructure.llm.prompts import PROMPT_REGISTRY
from src.infrastructure.llm.prompts.base import BASE_SYSTEM_PROMPT
from src.core.entities.analysis_request import AnalysisType
from src.core.entities.analysis_result import Finding, SeverityLevel
from src.config.settings import settings

logger = logging.getLogger(__name__)

class AnalyzerNode:
    def __init__(self, analysis_type: AnalysisType) -> None:
        self.analysis_type = analysis_type
        self._llm = ChatGoogleGenerativeAI(
            model=settings.gemini_model,
            google_api_key=settings.google_api_key,
            temperature=settings.llm_temperature,
            max_output_tokens=settings.llm_max_tokens,
        )

    async def run(self, state: AegisState) -> dict:
        request = state["request"]
        logger.info(f"[{self.analysis_type.value}_node] Analisando...")

        try:
            prompt_template = PROMPT_REGISTRY[self.analysis_type]
            human_message = prompt_template.format(
                title=request.title,
                description=request.description,
                context=json.dumps(request.context, ensure_ascii=False),
                depth=request.depth.value,
            )

            messages = [
                SystemMessage(content=BASE_SYSTEM_PROMPT),
                HumanMessage(content=human_message),
            ]

            response = await self._llm.ainvoke(messages)
            raw_content = self._extract_text(response.content)
            findings = self._parse_findings(raw_content)

            logger.info(
                f"[{self.analysis_type.value}_node] "
                f"{len(findings)} findings encontrados"
            )

            return {"raw_findings": findings}

        except Exception as e:
            logger.error(f"[{self.analysis_type.value}_node] Erro: {e}")
            return {
                "raw_findings": [],
                "errors": [f"{self.analysis_type.value}: {str(e)}"],
            }

    def _parse_findings(self, raw_content: str) -> list[Finding]:
        try:
            clean = self._clean_json(raw_content)
            data = json.loads(clean)

            return [
                Finding(
                    severity=SeverityLevel(f.get("severity", "info")),
                    category=f.get("category", self.analysis_type.value),
                    title=f.get("title", "Sem título"),
                    description=f.get("description", ""),
                    recommendation=f.get("recommendation", ""),
                    code_example=f.get("code_example"),
                )
                for f in data.get("findings", [])
            ]
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            logger.warning(f"Parse falhou para {self.analysis_type.value}: {e}")
            return []

    @staticmethod
    def _extract_text(content: object) -> str:
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            texts = []
            for item in content:
                if isinstance(item, dict) and item.get("type") == "text":
                    texts.append(item.get("text", ""))
                elif isinstance(item, str):
                    texts.append(item)
            return "\n".join(texts)
        return str(content)

    @staticmethod
    def _clean_json(raw: str) -> str:
        clean = raw.strip()
        if clean.startswith("```"):
            lines = clean.split("\n")
            clean = "\n".join(lines[1:-1]).strip()
        return clean

_architecture_analyzer  = AnalyzerNode(AnalysisType.ARCHITECTURE)
_solid_analyzer         = AnalyzerNode(AnalysisType.SOLID)
_performance_analyzer   = AnalyzerNode(AnalysisType.PERFORMANCE)
_security_analyzer      = AnalyzerNode(AnalysisType.SECURITY)
_data_pipeline_analyzer = AnalyzerNode(AnalysisType.DATA_PIPELINE)
_ai_system_analyzer     = AnalyzerNode(AnalysisType.AI_SYSTEM)

async def architecture_node(state: AegisState)  -> dict:
    return await _architecture_analyzer.run(state)

async def solid_node(state: AegisState) -> dict:
    return await _solid_analyzer.run(state)

async def performance_node(state: AegisState) -> dict:
    return await _performance_analyzer.run(state)

async def security_node(state: AegisState) -> dict:
    return await _security_analyzer.run(state)

async def data_pipeline_node(state: AegisState) -> dict:
    return await _data_pipeline_analyzer.run(state)

async def ai_system_node(state: AegisState) -> dict:
    return await _ai_system_analyzer.run(state)