from uuid import UUID
from pydantic import BaseModel


class Operation(BaseModel):
    operation_type: str
    amount: float


class WalletBalance(BaseModel):
    balance: float


class WalletModel(BaseModel):
    id: UUID
    balance: float

    class Config:
        from_attributes = True


