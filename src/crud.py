"""
src/crud.py
"""
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, APIRouter
from fastapi.responses import JSONResponse

from database import get_db
from models import Wallet

router = APIRouter()


def handle_exception(e):
    return JSONResponse(status_code=500, content={"message": f"Произошла неизвестная ошибка: {e}"})


@router.get("/get_wallet/{wallet_id}")
async def get_wallet(wallet_id: str, db: AsyncSession = Depends(get_db)):
    wallet_query = select(Wallet).where(Wallet.id == wallet_id)
    result = await db.execute(wallet_query)
    wallet = result.scalars().first()
    if not wallet:
        return JSONResponse(status_code=404, content={"message": "Кошелёк не найден"})
    return wallet


@router.post("/add_wallet/")
async def add_wallet(db: AsyncSession = Depends(get_db)):
    try:
        wallet_id = uuid.uuid4()
        new_wallet = Wallet(id=wallet_id, balance=0.0)
        db.add(new_wallet)
        await db.commit()
        await db.refresh(new_wallet)
        return {"id": new_wallet.id, "message": "Кошелёк успешно создан"}
    except Exception as e:
        await db.rollback()
        return handle_exception(e)


@router.post("/update_balance/{wallet_id}")
async def update_balance(wallet_id: str, amount:float, db: AsyncSession = Depends(get_db)):
    async with db.begin():
        try:
            result = await db.execute(select(Wallet).where(Wallet.id == wallet_id).with_for_update())
            wallet = result.scalars().first()
            if wallet:
                if wallet.balance + amount >= 0:
                    wallet.balance += amount
                    await db.commit()
                    return {"balance": wallet.balance}
                else:
                    return JSONResponse(status_code=400, content={"message": f"Не хватает средств для снятия"})
            else:
                return JSONResponse(status_code=404, content={"message": f"Кошелек не найден"})
        except Exception as e:
            return handle_exception(e)
