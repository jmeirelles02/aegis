import pytest
from httpx import AsyncClient

class TestHealthEndpoint:

    @pytest.mark.asyncio
    async def test_health_returns_200(self, client: AsyncClient):
        response = await client.get("/health")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_health_schema(self, client: AsyncClient):
        response = await client.get("/health")
        data = response.json()

        assert "status" in data
        assert "llm_available" in data
        assert "version" in data

class TestAnalysisEndpoints:

    @pytest.mark.asyncio
    async def test_create_analysis_returns_201(self, client: AsyncClient):
        payload = {
            "title": "Sistema de Teste",
            "description": "Monolito FastAPI com PostgreSQL e sem cache nem filas de mensageria.",
            "analysis_types": ["architecture"],
            "depth": "standard",
            "context": {},
        }
        response = await client.post("/analyses/", json=payload)
        assert response.status_code == 201

    @pytest.mark.asyncio
    async def test_create_analysis_response_schema(self, client: AsyncClient):
        payload = {
            "title": "Sistema de Teste",
            "description": "Monolito FastAPI com PostgreSQL e sem cache nem filas de mensageria.",
            "analysis_types": ["architecture"],
            "depth": "standard",
            "context": {},
        }
        response = await client.post("/analyses/", json=payload)
        data = response.json()

        assert "id" in data
        assert "findings" in data
        assert "summary" in data
        assert "has_critical_issues" in data
        assert "processing_time_ms" in data
        assert "created_at" in data

    @pytest.mark.asyncio
    async def test_create_analysis_invalid_title(self, client: AsyncClient):
        payload = {
            "title": "A",# muito curto
            "description": "Monolito FastAPI com PostgreSQL e sem cache nem filas.",
            "analysis_types": ["architecture"],
        }
        response = await client.post("/analyses/", json=payload)
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_list_analyses_returns_200(self, client: AsyncClient):
        response = await client.get("/analyses/")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_list_analyses_schema(self, client: AsyncClient):
        response = await client.get("/analyses/")
        data = response.json()

        assert "total" in data
        assert "analyses" in data
        assert isinstance(data["analyses"], list)

    @pytest.mark.asyncio
    async def test_get_analysis_by_id(self, client: AsyncClient):
        response = await client.get("/analyses/any-id")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_get_analysis_not_found(self, client: AsyncClient, mock_repository):
        mock_repository.find_by_id.return_value = None
        response = await client.get("/analyses/id-inexistente")
        assert response.status_code == 404