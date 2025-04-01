"""
src/crud.py
"""

import uuid
from decimal import Decimal

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


def validate_uuid(uuid_to_test: str) -> UUID:
    try:
        return uuid.UUID(uuid_to_test, version=4)
    except (ValueError, DataError):
        raise HTTPException(status_code=400, detail="Некорректный UUID")


@router.post("/api/v1/add_wallet/")
async def add_wallet(db: AsyncSession = Depends(get_db)):
    new_wallet = Wallet()
    db.add(new_wallet)
    await db.commit()
    return JSONResponse(
        status_code=200,
        content={"id": str(new_wallet.id), "message": "Кошелёк успешно создан"},
    )


@router.get("/api/v1/wallets/{wallet_id}", response_model=WalletModel)
async def get_wallet(wallet_id: str, db: AsyncSession = Depends(get_db)):
    validated_uuid = validate_uuid(wallet_id)

    wallet_query = select(Wallet).where(Wallet.id == validated_uuid)
    result = await db.execute(wallet_query)
    wallet = result.scalars().first()

    if not wallet:
        raise HTTPException(status_code=404, detail="Кошелёк не найден")

    return WalletModel.from_orm(wallet)


@router.post("/api/v1/wallets/{wallet_id}/operation")
async def update_balance(
    wallet_id: str, operation: Operation, db: AsyncSession = Depends(get_db)
):
    try:
        operation_type = operation.operation_type
        amount = Decimal(operation.amount)

        if operation_type not in ["DEPOSIT", "WITHDRAW"]:
            raise HTTPException(status_code=400, detail="Некорректный тип операции")
        if amount <= Decimal("0.00"):
            raise HTTPException(
                status_code=400,
                detail=f"Сумма {operation_type} должна быть положительной",
            )

        async with db.begin():
            wallet_query = (
                select(Wallet).where(Wallet.id == wallet_id).with_for_update()
            )
            result = await db.execute(wallet_query)
            existing_wallet = result.scalars().first()

            if not existing_wallet:
                raise HTTPException(status_code=404, detail="Кошелек не найден")

            if operation_type == "DEPOSIT":
                existing_wallet.balance += amount
            elif operation_type == "WITHDRAW":
                if existing_wallet.balance < amount:
                    raise HTTPException(
                        status_code=400, detail="Не хватает средств для снятия"
                    )
                existing_wallet.balance -= amount

        return JSONResponse(
            status_code=200,
            content={
                "message": "Операция проведена успешно",
                "balance": str(existing_wallet.balance),
            },
        )

    except Exception as e:
        logging.error(f"Ошибка при обновлении баланса: {e}")
        raise HTTPException(
            status_code=500, detail=f"Произошла ошибка при обработке запроса: {e}"
        )
