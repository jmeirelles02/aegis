from fastapi import APIRouter, HTTPException, status
from src.api.schemas import (
    AnalysisRequestSchema,
    AnalysisResponse,
    AnalysisListResponse,
    ErrorResponse,
)
from src.api.mappers import to_analysis_response
from src.core.dependencies import (
    get_analyze_use_case,
    get_get_analysis_use_case,
    get_list_analyses_use_case,
)
from src.core.entities.analysis_request import AnalysisRequest

router = APIRouter(prefix="/analyses", tags=["Analysis"])

@router.post(
    "/",
    response_model=AnalysisResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Analisar Arquitetura",
    description="Submete uma proposta de arquitetura para análise pelo Aegis Shadow Architect.",
    responses={
        400: {"model": ErrorResponse, "description": "Request inválido"},
        422: {"description": "Erro de validação"},
        500: {"model": ErrorResponse, "description": "Erro interno"},
    },
)
async def create_analysis(body: AnalysisRequestSchema) -> AnalysisResponse:
    """
    Executa análise completa da arquitetura submetida.
    Retorna findings, score e veredicto do Shadow Architect.
    """
    try:
        use_case = get_analyze_use_case()

        request = AnalysisRequest(
            title=body.title,
            description=body.description,
            analysis_types=body.analysis_types,
            depth=body.depth,
            context=body.context,
        )

        result = await use_case.execute(request)
        return to_analysis_response(result)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}",
        )

@router.get(
    "/",
    response_model=AnalysisListResponse,
    summary="Listar Análises",
    description="Retorna todas as análises realizadas na sessão atual.",
)
async def list_analyses() -> AnalysisListResponse:
    """Lista todas as análises realizadas."""
    try:
        use_case = get_list_analyses_use_case()
        results = await use_case.execute()

        return AnalysisListResponse(
            total=len(results),
            analyses=[to_analysis_response(r) for r in results],
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}",
        )

@router.get(
    "/{analysis_id}",
    response_model=AnalysisResponse,
    summary="Buscar Análise por ID",
    responses={
        404: {"model": ErrorResponse, "description": "Análise não encontrada"},
    },
)
async def get_analysis(analysis_id: str) -> AnalysisResponse:
    """Recupera uma análise específica pelo ID."""
    try:
        use_case = get_get_analysis_use_case()
        result = await use_case.execute(analysis_id)
        return to_analysis_response(result)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}",
        )