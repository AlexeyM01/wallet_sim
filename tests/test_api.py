"""
tests/test_api.py
"""
import pytest
import uuid
from fastapi import status


@pytest.mark.asyncio
async def test_add_wallet(async_client):
    add_wallet_response = await async_client.post("/api/v1/add_wallet/")
    assert add_wallet_response.status_code == status.HTTP_200_OK
    data = add_wallet_response.json()
    assert "id" in data
    assert "message" in data
    assert data["message"] == "Кошелёк успешно создан"


@pytest.mark.asyncio
async def test_get_wallet_correct(async_client):
    add_wallet_response = await async_client.post("/api/v1/add_wallet/")
    wallet_id = add_wallet_response.json()["id"]

    response = await async_client.get(f"/api/v1/wallets/{wallet_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == str(wallet_id)
    assert data["balance"] == 0.0


@pytest.mark.asyncio
async def test_get_wallet_invalid_uuid(async_client):
    response = await async_client.get("/api/v1/wallets/Некорректный_UUID")
    assert response.status_code == 400
    assert response.json()["detail"] == "Некорректный UUID"


@pytest.mark.asyncio
async def test_get_wallet_not_found(async_client):
    invalid_wallet_id = uuid.uuid4()
    response = await async_client.get(f"/api/v1/wallets/{invalid_wallet_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Кошелёк не найден"


@pytest.mark.asyncio
async def test_update_balance_correct_deposit(async_client):
    create_response = await async_client.post("api/v1/add_wallet/")
    wallet_id = uuid.UUID(create_response.json()["id"])

    update_response = await async_client.post(
        f"/api/v1/wallets/{wallet_id}/operation",
        json={"operation_type": "DEPOSIT", "amount": 100}
    )
    assert update_response.status_code == status.HTTP_200_OK
    assert update_response.json()["balance"] == 100.0


@pytest.mark.asyncio
async def test_update_balance_correct_withdraw(async_client):
    create_response = await async_client.post("api/v1/add_wallet/")
    wallet_id = uuid.UUID(create_response.json()["id"])

    await async_client.post(
        f"/api/v1/wallets/{wallet_id}/operation",
        json={"operation_type": "DEPOSIT", "amount": 200}
    )

    update_response = await async_client.post(
        f"/api/v1/wallets/{wallet_id}/operation",
        json={"operation_type": "WITHDRAW", "amount": 150}
    )
    assert update_response.status_code == status.HTTP_200_OK
    assert update_response.json()["balance"] == 50.0


@pytest.mark.asyncio
async def test_update_balance_withdraw_not_enough_funds(async_client):
    create_response = await async_client.post("/api/v1/add_wallet/")
    wallet_id = uuid.UUID(create_response.json()["id"])

    update_response = await async_client.post(
        f"/api/v1/wallets/{wallet_id}/operation",
        json={"operation_type": "WITHDRAW", "amount": 100}
    )
    assert update_response.status_code == status.HTTP_400_BAD_REQUEST
    assert update_response.json()["detail"] == "Не хватает средств для снятия"


@pytest.mark.asyncio
async def test_update_balance_invalid_operation(async_client):
    create_response = await async_client.post("/api/v1/add_wallet/")
    wallet_id = uuid.UUID(create_response.json()["id"])

    update_response = await async_client.post(
        f"/api/v1/wallets/{wallet_id}/operation",
        json={"operation_type": "INVALID_OPERATION", "amount": 100}
    )
    assert update_response.status_code == status.HTTP_400_BAD_REQUEST
    assert update_response.json()["detail"] == "Некорректный тип операции"


@pytest.mark.asyncio
async def test_update_balance_negative_amount(async_client):
    create_response = await async_client.post("/api/v1/add_wallet/")
    wallet_id = uuid.UUID(create_response.json()["id"])

    update_response = await async_client.post(
        f"/api/v1/wallets/{wallet_id}/operation",
        json={"operation_type": "DEPOSIT", "amount": -50}
    )
    assert update_response.status_code == status.HTTP_400_BAD_REQUEST
    assert update_response.json()["detail"] == "Сумма DEPOSIT должна быть положительной"


@pytest.mark.asyncio
async def test_update_balance_zero_amount(async_client):
    create_response = await async_client.post("/api/v1/add_wallet/")
    wallet_id = uuid.UUID(create_response.json()["id"])

    update_response = await async_client.post(
        f"/api/v1/wallets/{wallet_id}/operation",
        json={"operation_type": "DEPOSIT", "amount": 0}
    )
    assert update_response.status_code == status.HTTP_400_BAD_REQUEST
    assert update_response.json()["detail"] == "Сумма DEPOSIT должна быть положительной"
