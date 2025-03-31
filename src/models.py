from decimal import Decimal
from sqlalchemy import Column, UUID, Numeric
from database import Base
import uuid


class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    balance = Column(Numeric(precision=10, scale=2), default=Decimal("0.00"))

    def __repr__(self):
        return f"<Wallet(id={self.id}, balance={self.balance})>"
