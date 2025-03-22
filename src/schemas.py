from pydantic import BaseModel


class Operation(BaseModel):
    operation_type: str
    amount: float


class WalletBalance(BaseModel):
    balance: float
