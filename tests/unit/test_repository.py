import pytest
from src.infrastructure.repositories.in_memory_repository import (
    InMemoryAnalysisRepository,
)

class TestInMemoryRepository:

    @pytest.mark.asyncio
    async def test_save_and_find(self, sample_result):
        repo = InMemoryAnalysisRepository()
        saved = await repo.save(sample_result)
        found = await repo.find_by_id(saved.id)

        assert found is not None
        assert found.id == sample_result.id

    @pytest.mark.asyncio
    async def test_find_not_found_returns_none(self):
        repo = InMemoryAnalysisRepository()
        result = await repo.find_by_id("nao-existe")
        assert result is None

    @pytest.mark.asyncio
    async def test_list_all_empty(self):
        repo = InMemoryAnalysisRepository()
        results = await repo.list_all()
        assert results == []

    @pytest.mark.asyncio
    async def test_list_all_after_save(self, sample_result):
        repo = InMemoryAnalysisRepository()
        await repo.save(sample_result)
        results = await repo.list_all()

        assert len(results) == 1
        assert results[0].id == sample_result.id

    @pytest.mark.asyncio
    async def test_save_multiple(self, sample_result):
        import copy
        import uuid

        repo = InMemoryAnalysisRepository()
        result2 = copy.deepcopy(sample_result)
        result2.__dict__["id"] = str(uuid.uuid4())

        await repo.save(sample_result)
        await repo.save(result2)

        results = await repo.list_all()
        assert len(results) == 2