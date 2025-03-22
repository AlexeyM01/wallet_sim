from sqlalchemy import Column, Float, Integer, UUID
from database import Base
import uuid


class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    balance = Column(Float, default=0.0)

    def __repr__(self):
        return f"<Wallet(id={self.id}, balance={self.balance})>"