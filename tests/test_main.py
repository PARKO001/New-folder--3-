import uuid

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app

pytestmark = pytest.mark.asyncio


class TestUPICRUD:
    # Generate unique UPI ID per test class
    unique_upi_id = f"testuser_{uuid.uuid4().hex[:6]}@upi"
    valid_data = {"name": "Test User", "upi_id": unique_upi_id}
    updated_data = {
        "name": "Updated User",
        "upi_id": f"updated_{uuid.uuid4().hex[:6]}@upi",
    }
    invalid_data = {"name": "", "upi_id": ""}

    @staticmethod
    async def get_test_client():
        transport = ASGITransport(app=app)
        return AsyncClient(transport=transport, base_url="http://test")

    async def test_create_upi(self):
        async with await self.get_test_client() as ac:
            response = await ac.post("/upi/", json=self.valid_data)
        assert response.status_code == 200
        assert "message" in response.json()

    async def test_read_upi(self):
        async with await self.get_test_client() as ac:
            response = await ac.get("/upi/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    async def test_update_upi(self):
        async with await self.get_test_client() as ac:
            response = await ac.put("/upi/1", json=self.updated_data)
        assert response.status_code in (200, 400)

    async def test_delete_upi(self):
        async with await self.get_test_client() as ac:
            response = await ac.delete("/upi/1")
        assert response.status_code in (200, 400)

    async def test_create_upi_sql_failure(self, monkeypatch):
        def mock_cursor_execute_fail(*args, **kwargs):
            raise Exception("Simulated SQL Error")

        class MockCursor:
            def execute(self, *args, **kwargs):
                raise Exception("Simulated SQL Error")

            def close(self):
                pass

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc_val, exc_tb):
                pass

        class MockConn:
            def cursor(self):
                return MockCursor()

            def commit(self):
                pass

            def close(self):
                pass

        monkeypatch.setattr("app.crud.get_connection", lambda: MockConn())

        async with await self.get_test_client() as ac:
            response = await ac.post("/upi/", json=self.valid_data)

        assert response.status_code == 400
        assert "Simulated SQL Error" in response.json()["detail"]

    async def test_update_upi_exception(self, monkeypatch):
        def mock_update_upi(id, name, upi_id):
            raise Exception("DB update error")

        monkeypatch.setattr("app.crud.update_upi", mock_update_upi)

        async with await self.get_test_client() as ac:
            response = await ac.put("/upi/99999", json=self.updated_data)
        assert response.status_code == 400
        assert response.json()["detail"] == "DB update error"

    async def test_delete_upi_exception(self, monkeypatch):
        def mock_delete_upi(id):
            raise Exception("DB delete error")

        monkeypatch.setattr("app.crud.delete_upi", mock_delete_upi)

        async with await self.get_test_client() as ac:
            response = await ac.delete("/upi/99999")
        assert response.status_code == 400
        assert response.json()["detail"] == "DB delete error"

    async def test_create_upi_validation_failure(self):
        async with await self.get_test_client() as ac:
            response = await ac.post("/upi/", json=self.invalid_data)
        assert response.status_code == 422

    async def test_update_nonexistent_id(self):
        async with await self.get_test_client() as ac:
            response = await ac.put("/upi/999999", json=self.updated_data)
        assert response.status_code in (200, 400)

    async def test_delete_nonexistent_id(self):
        async with await self.get_test_client() as ac:
            response = await ac.delete("/upi/999999")
        assert response.status_code in (200, 400)

    async def test_read_upi_empty(self, monkeypatch):
        monkeypatch.setattr("app.crud.get_all_upi", lambda: [])
        async with await self.get_test_client() as ac:
            response = await ac.get("/upi/")
        assert response.status_code == 200
        assert response.json() == []

    async def test_create_duplicate_upi(self):
        async with await self.get_test_client() as ac:
            await ac.post("/upi/", json=self.valid_data)
            response = await ac.post("/upi/", json=self.valid_data)
        assert response.status_code in (400, 409)

    async def test_update_upi_validation_failure(self):
        async with await self.get_test_client() as ac:
            response = await ac.put("/upi/1", json=self.invalid_data)
        assert response.status_code == 422


# random text for testing purpose
# This is a placeholder for any additional text or comments.
# You can replace this with any other text or leave it empty.
# This is a placeholder for any additional text or comments.
# You can replace this with any other text or leave it empty.
