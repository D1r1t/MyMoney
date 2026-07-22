from ..models.base             import Base
from sqlalchemy.orm    import Mapped, mapped_column
from sqlalchemy        import String, ForeignKey, Integer
from ..models.currency import Currency
from datetime          import datetime

class AnaliticByDay(Base):
    __tablename__ = "analitic_by_day"

    rec_date: Mapped[datetime]         = mapped_column(primary_key=True)
    acc_name: Mapped[str]              = mapped_column(primary_key=True)
    cat_name: Mapped[int]              = mapped_column(primary_key=True)
    income_plan: Mapped[Integer]       = mapped_column(Integer)
    income_fact: Mapped[Integer]       = mapped_column(Integer)
    income_deviation: Mapped[Integer]  = mapped_column(Integer)
    expense_plan: Mapped[Integer]      = mapped_column(Integer)
    expense_fact: Mapped[Integer]      = mapped_column(Integer)
    expense_deviation: Mapped[Integer] = mapped_column(Integer)
