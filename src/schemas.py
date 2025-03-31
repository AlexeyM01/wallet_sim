from typing import Literal
from uuid import UUID
from decimal import Decimal
from pydantic import BaseModel, condecimal


class Operation(BaseModel):
    operation_type: Literal["DEPOSIT", "WITHDRAW"]
    amount: condecimal(decimal_places=2)

    class Config:
        from_attributes = True


class WalletBalance(BaseModel):
    balance: condecimal(decimal_places=2)


class WalletModel(BaseModel):
    id: UUID
    balance: condecimal(decimal_places=2)

    class Config:
        from_attributes = True
