# src/infrastructure/graph/nodes/aggregator_node.py

import logging
from src.infrastructure.graph.state import AegisState
from src.core.entities.analysis_result import SeverityLevel, Finding

logger = logging.getLogger(__name__)

SEVERITY_ORDER = {
    SeverityLevel.CRITICAL: 0,
    SeverityLevel.HIGH:     1,
    SeverityLevel.MEDIUM:   2,
    SeverityLevel.LOW:      3,
    SeverityLevel.INFO:     4,
}


def _deduplicate_findings(findings: list[Finding]) -> list[Finding]:
    """Remove duplicatas por título + categoria."""
    seen: dict[str, Finding] = {}

    for finding in findings:
        key = f"{finding.title.lower().strip()}|{finding.category.lower().strip()}"

        if key not in seen:
            seen[key] = finding
        else:
            existing_priority = SEVERITY_ORDER.get(seen[key].severity, 99)
            new_priority = SEVERITY_ORDER.get(finding.severity, 99)
            if new_priority < existing_priority:
                seen[key] = finding

    return list(seen.values())


async def aggregator_node(state: AegisState) -> dict:
    """
    Lê raw_findings (acumulados), deduplica e
    escreve em findings (lista final limpa).
    """
    # ✅ Lê de raw_findings
    raw_findings = state.get("raw_findings", [])

    unique_findings = _deduplicate_findings(raw_findings)

    sorted_findings = sorted(
        unique_findings,
        key=lambda f: SEVERITY_ORDER.get(f.severity, 99),
    )

    critical_count = sum(
        1 for f in sorted_findings
        if f.severity == SeverityLevel.CRITICAL
    )

    logger.info(
        f"[aggregator_node] "
        f"{len(raw_findings)} brutos → "
        f"{len(sorted_findings)} únicos | "
        f"{critical_count} críticos"
    )

    # ✅ Escreve em findings (substitui, não acumula)
    return {
        "findings": sorted_findings,
        "current_step": "summarizing",
    }