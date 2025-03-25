"""
tests/conftest.py
"""
import httpx
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db, create_test_database, drop_test_database


@pytest.fixture(scope="function")
async def async_client():
    async with AsyncClient(base_url="http://127.0.0.1:8080") as client:
        try:
            response = await client.get("/")
            response.raise_for_status()
        except httpx.ConnectError as e:
            print(f"Ошибка подключения: {e}")
            pytest.fail(f"Не удалось подключиться к серверу: {e}")
        except httpx.HTTPStatusError as e:
            print(f"Ошибка HTTP: {e}")
            pytest.fail(f"Ошибка HTTP: {e}")
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            pytest.fail(f"Произошла ошибка: {e}")

        yield client


@pytest.fixture(scope="function", autouse=True)
async def setup_database():
    await create_test_database()
    yield
    await drop_test_database()


@pytest.fixture
async def db_session() -> AsyncSession:
    async with get_db() as session:
        yield session
