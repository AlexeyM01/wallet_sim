from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
import crud
import schemas
from database import get_db
from main import app


@app.post("/api/v1/wallets/{wallet_id}/operation")
async def perform_operation(wallet_id: int, operation: schemas.Operation, db: Session = Depends(get_db)):
    if operation.operation_type not in ["DEPOSIT", "WITHDRAW"]:
        raise HTTPException(status_code=400, detail="Invalid operation type")
    amount = operation.amount if operation.operation_type == "DEPOSIT" else -operation.amount
    with db.begin():
        new_balance = crud.update_balance(wallet_id, amount)
    if new_balance is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return {"new_balance": new_balance}


@app.get("/api/v1/wallets/{wallet_id}", response_model=schemas.WalletBalance)
async def get_balance(wallet_id: str, db: Session = Depends(get_db)):
    wallet = crud.get_wallet(db, wallet_id)
    if wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")

    return {"balance": wallet.balance}
