"""
src/crud.py
"""
import uuid

from asyncpg.exceptions import DataError
from sqlalchemy import select, UUID
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, APIRouter, HTTPException
from fastapi.responses import JSONResponse

from database import get_db
from models import Wallet
from schemas import WalletModel, Operation
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


def validate_uuid(uuid_to_test: str) -> UUID | None:
    try:
        return uuid.UUID(uuid_to_test, version=4)
    except (ValueError, DataError):
        return None


@router.post("/api/v1/add_wallet/")
async def add_wallet(db: AsyncSession = Depends(get_db)):
    new_wallet = Wallet(balance=0.0)
    db.add(new_wallet)
    await db.commit()
    return JSONResponse(status_code=200, content={
        "id": str(new_wallet.id), "message": "Кошелёк успешно создан"})


@router.get("/api/v1/wallets/{wallet_id}", response_model=WalletModel)
async def get_wallet(wallet_id: str, db: AsyncSession = Depends(get_db)):
    validated_uuid = validate_uuid(wallet_id)
    if validated_uuid is None:
        raise HTTPException(status_code=400, detail="Некорректный UUID")

    wallet_query = select(Wallet).where(Wallet.id == validated_uuid)
    result = await db.execute(wallet_query)
    wallet = result.scalars().first()

    if not wallet:
        raise HTTPException(status_code=404, detail="Кошелёк не найден")

    return WalletModel.from_orm(wallet)


@router.post("/api/v1/wallets/{wallet_id}/operation")
async def update_balance(wallet_id: str, operation: Operation, db: AsyncSession = Depends(get_db)):
    operation_type = operation.operation_type
    amount = operation.amount
    if operation_type not in ["DEPOSIT", "WITHDRAW"]:
        raise HTTPException(status_code=400, detail="Некорректный тип операции")

    if amount <= 0:
        raise HTTPException(status_code=400, detail=f"Сумма {operation_type} должна быть положительной")

    wallet_model = await get_wallet(wallet_id, db)
    new_balance = wallet_model.balance
    if operation_type == "DEPOSIT":
        new_balance += amount
    elif operation_type == "WITHDRAW":
        new_balance -= amount
        if new_balance < 0:
            raise HTTPException(status_code=400, detail="Не хватает средств для снятия")

    wallet_query = select(Wallet).where(Wallet.id == wallet_model.id)
    result = await db.execute(wallet_query)
    existing_wallet = result.scalars().first()

    existing_wallet.balance = new_balance
    await db.commit()
    await db.refresh(existing_wallet)

    return JSONResponse(status_code=200, content={"message": "Операция проведена успешно",
                                                  "balance": existing_wallet.balance})
