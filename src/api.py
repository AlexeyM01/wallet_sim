"""
src/api.py
"""
from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

import crud
import schemas
from database import get_db

router = APIRouter()


@router.post("/v1/add_wallet/")
async def add_wallet(db: AsyncSession = Depends(get_db)):
    try:
        response = crud.add_wallet(db)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/v1/wallets/{wallet_id}/operation")
async def perform_operation(wallet_id: str, operation: schemas.Operation, db: AsyncSession = Depends(get_db)):
    if operation.operation_type not in ["DEPOSIT", "WITHDRAW"]:
        raise HTTPException(status_code=400, detail="Invalid operation type")
    if operation.amount <= 0:
        raise HTTPException(status_code=400, detail=f"Сумма {operation.operation_type} должна быть положительной")

    amount = operation.amount if operation.operation_type == "DEPOSIT" else -operation.amount
    with db.begin():
        response = await crud.update_balance(wallet_id, amount, db)
        new_balance = response["balance"]
        return {"new_balance": new_balance}


@router.get("/v1/wallets/{wallet_id}")
async def get_balance(wallet_id: str, db: AsyncSession = Depends(get_db)):
    wallet = crud.get_wallet(wallet_id, db)
    return {"balance": wallet.balance}
