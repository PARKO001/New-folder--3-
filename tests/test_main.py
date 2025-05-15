import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
import uuid

pytestmark = pytest.mark.asyncio

# Generate unique UPI ID for each test run
unique_upi_id = f"testuser_{uuid.uuid4().hex[:6]}@upi"

# Sample test data
valid_data = {"name": "Test User", "upi_id": unique_upi_id}
updated_data = {"name": "Updated User", "upi_id": f"updated_{uuid.uuid4().hex[:6]}@upi"}
invalid_data = {"name": "", "upi_id": ""}

# Helper function to get a test client
async def get_test_client():
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


# Test: Create UPI (Valid)
async def test_create_upi():
    async with await get_test_client() as ac:
        response = await ac.post("/upi/", json=valid_data)
    assert response.status_code == 200
    assert "message" in response.json()


# Test: Read UPI
async def test_read_upi():
    async with await get_test_client() as ac:
        response = await ac.get("/upi/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# Test: Update UPI
async def test_update_upi():
    async with await get_test_client() as ac:
        response = await ac.put("/upi/1", json=updated_data)
    assert response.status_code in (200, 400)  


# Test: Delete UPI
async def test_delete_upi():
    async with await get_test_client() as ac:
        response = await ac.delete("/upi/1")
    assert response.status_code in (200, 400) 


# Test: Invalid input for create
async def test_invalid_input_create():
    async with await get_test_client() as ac:
        response = await ac.post("/upi/", json=invalid_data)
    assert response.status_code == 422


# Test: Force exception in create
async def test_create_upi_exception(monkeypatch):
    def mock_create_upi(name, upi_id):
        raise Exception("DB insert error")

    monkeypatch.setattr("app.crud.create_upi", mock_create_upi)

    async with await get_test_client() as ac:
        response = await ac.post("/upi/", json=valid_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "DB insert error"


# Test: Force exception in update
async def test_update_upi_exception(monkeypatch):
    def mock_update_upi(id, name, upi_id):
        raise Exception("DB update error")

    monkeypatch.setattr("app.crud.update_upi", mock_update_upi)

    async with await get_test_client() as ac:
        response = await ac.put("/upi/99999", json=updated_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "DB update error"


# Test: Force exception in delete
async def test_delete_upi_exception(monkeypatch):
    def mock_delete_upi(id):
        raise Exception("DB delete error")

    monkeypatch.setattr("app.crud.delete_upi", mock_delete_upi)

    async with await get_test_client() as ac:
        response = await ac.delete("/upi/99999")
    assert response.status_code == 400
    assert response.json()["detail"] == "DB delete error"