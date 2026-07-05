from base           import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy     import String, DateTime, Integer, ForeignKey
from datetime       import date, datetime
from currency       import Currency

class Exchange_rates(Base):
    __tablename__ = "exchange_rates"

    id: Mapped[int]                  = mapped_column(primary_key=True)
    rate_date: Mapped[datetime]      = mapped_column(DateTime)
    main_currency_id: Mapped[int]    = mapped_column(ForeignKey("currency.id"))
    current_currency_id: Mapped[int] = mapped_column(ForeignKey("currency.id"))
    rare: Mapped[int]                = mapped_column(Integer)

    main_currency: Mapped["Currency"]    = relationship()
    current_currency: Mapped["Currency"] = relationship()

    def __init__(self, rate_date: datetime, main_currency: Currency, current_currency: Currency, rare: int):
        self.rate_date        = rate_date
        self.main_currency    = main_currency
        self.current_currency = current_currency
        self.rare             = rare

    @classmethod
    def from_dict(cls, data: dict):
        cls(
            rate_date        = data["rate_date"],
            main_currency    = data["main_currency"],
            current_currency = data["current_currency"],
            rare             = data["rare"]
        )

    def __repr__(self) -> str:
        return (
            f"Exchange_rates(id = {self.id}, rate_date = {self.rate_date}," 
            f"main_currency_id = {self.main_currency_id}, current_currency_id ={self.current_currency_id})"
            f"rate = {self.rare}"
        )

        