from base           import Base
from sqlalchemy.org import Mapped, mapped_column
from sqlalchemy     import String, DateTime, Integer, ForeignKey
from datetime       import date, datetime

class Exchange_rates(Base.Base):
    __tablename__ = "currency"

    id: Mapped[int]               = mapped_column(primary_key=True)
    rate_date: Mapped[datetime]   = mapped_column(DateTime)
    main_currency: Mapped[int]    = mapped_column(ForeignKey("Currency.id"))
    current_currency: Mapped[int] = mapped_column(ForeignKey("Currency.id"))
    rare: Mapped[int]             = mapped_column(Integer)