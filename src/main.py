import uuid

from fastapi import FastAPI, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from crud import router as crud_router
from database import get_db
from models import Wallet

app = FastAPI()
app.include_router(crud_router)


@app.get("/db-status")
async def check_db_connection(db: AsyncSession = Depends(get_db)):
    """Функция-проверка соединения с базой данных"""
    try:
        wallet_id = uuid.uuid4()
        wallet_query = select(Wallet).where(Wallet.id == wallet_id)
        result = await db.execute(wallet_query)
        wallet = result.scalars().first()
        return JSONResponse(status_code=200, content={"message": "Подключение к базе данных успешно"})
    except Exception as e:
        return JSONResponse(status_code=500, content=f"При подключении к базе данных произошла ошибка {e}")
