from base           import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy     import String, ForeignKey
from currency       import Currency

class Accounts(Base):
    __tablename__ = "accounts"

    id: Mapped[int]          = mapped_column(primary_key=True)
    acc_name: Mapped[str]    = mapped_column(String(150))
    currency_id: Mapped[int] = mapped_column(ForeignKey("currency.id"))

    currency: Mapped["Currency"] = relationship()

    def __init__(self, acc_name: str, currency: Currency):
        self.acc_name = acc_name
        self.currency = currency

    def __repr__(self) -> str:
        return f"Account(id = {self.id}, acc_name = {self.acc_name}, currency_id = {self.currency_id})"