import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
import uuid

pytestmark = pytest.mark.asyncio


class TestUPICRUD:
    # Generate unique UPI ID per test class
    unique_upi_id = f"testuser_{uuid.uuid4().hex[:6]}@upi"
    valid_data = {"name": "Test User", "upi_id": unique_upi_id}
    updated_data = {"name": "Updated User", "upi_id": f"updated_{uuid.uuid4().hex[:6]}@upi"}
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

    async def test_invalid_input_create(self):
        async with await self.get_test_client() as ac:
            response = await ac.post("/upi/", json=self.invalid_data)
        assert response.status_code == 422

    async def test_create_upi_exception(self, monkeypatch):
        def mock_create_upi(name, upi_id):
            raise Exception("DB insert error")

        monkeypatch.setattr("app.crud.create_upi", mock_create_upi)

        async with await self.get_test_client() as ac:
            response = await ac.post("/upi/", json=self.valid_data)
        assert response.status_code == 400
        assert response.json()["detail"] == "DB insert error"

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
