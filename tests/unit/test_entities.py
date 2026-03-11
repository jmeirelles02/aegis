import pytest
from src.core.entities.analysis_request import (
    AnalysisRequest,
    AnalysisType,
    AnalysisDepth,
)
from src.core.entities.analysis_result import (
    AnalysisResult,
    Finding,
    AnalysisSummary,
    SeverityLevel,
)

class TestAnalysisRequest:

    def test_create_valid_request(self):
        request = AnalysisRequest(
            title="Teste",
            description="Sistema monolítico com banco de dados único e sem cache.",
            analysis_types=[AnalysisType.ARCHITECTURE],
        )
        assert request.title == "Teste"
        assert request.depth == AnalysisDepth.STANDARD

    def test_default_analysis_type(self):
        request = AnalysisRequest(
            title="Teste",
            description="Sistema monolítico com banco de dados único e sem cache.",
        )
        assert request.analysis_types == [AnalysisType.ARCHITECTURE]

    def test_description_too_short_raises(self):
        with pytest.raises(Exception):
            AnalysisRequest(
                title="Teste",
                description="curta",
            )

    def test_multiple_analysis_types(self):
        request = AnalysisRequest(
            title="Teste",
            description="Sistema monolítico com banco de dados único e sem cache.",
            analysis_types=[
                AnalysisType.ARCHITECTURE,
                AnalysisType.SECURITY,
                AnalysisType.SOLID,
            ],
        )
        assert len(request.analysis_types) == 3

    def test_context_default_empty(self):
        request = AnalysisRequest(
            title="Teste",
            description="Sistema monolítico com banco de dados único e sem cache.",
        )
        assert request.context == {}

class TestAnalysisResult:

    def test_has_critical_issues_true(self, sample_finding, sample_summary):
        result = AnalysisResult(
            request_title="Teste",
            analysis_types=["architecture"],
            findings=[sample_finding],# critical
            summary=sample_summary,
            raw_response="",
            processing_time_ms=100,
        )
        assert result.has_critical_issues is True

    def test_has_critical_issues_false(self, sample_summary):
        low_finding = Finding(
            severity=SeverityLevel.LOW,
            category="Style",
            title="Naming",
            description="Nome de variável ruim.",
            recommendation="Use nomes descritivos.",
        )
        result = AnalysisResult(
            request_title="Teste",
            analysis_types=["architecture"],
            findings=[low_finding],
            summary=sample_summary,
            raw_response="",
            processing_time_ms=100,
        )
        assert result.has_critical_issues is False

    def test_findings_by_severity(self, sample_finding, sample_summary):
        medium_finding = Finding(
            severity=SeverityLevel.MEDIUM,
            category="Arch",
            title="Acoplamento",
            description="Módulos muito acoplados.",
            recommendation="Use interfaces.",
        )
        result = AnalysisResult(
            request_title="Teste",
            analysis_types=["architecture"],
            findings=[sample_finding, medium_finding],
            summary=sample_summary,
            raw_response="",
            processing_time_ms=100,
        )
        by_severity = result.findings_by_severity
        assert "critical" in by_severity
        assert "medium" in by_severity
        assert len(by_severity["critical"]) == 1
        assert len(by_severity["medium"]) == 1

    def test_result_has_uuid(self, sample_result):
        assert len(sample_result.id) == 36# UUID format