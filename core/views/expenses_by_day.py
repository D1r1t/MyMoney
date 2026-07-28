from ..models.base     import Base
from sqlalchemy.orm    import Mapped, mapped_column
from sqlalchemy        import String, ForeignKey, Integer
from ..models.currency import Currency
from datetime          import datetime

# ================================================================================

class ExpensesByDay(Base):
    __tablename__ = "expenses_by_day"

    rec_date: Mapped[datetime]         = mapped_column(primary_key=True)
    acc_name: Mapped[str]              = mapped_column(primary_key=True)
    cat_name: Mapped[int]              = mapped_column(primary_key=True)
    expense:  Mapped[Integer]          = mapped_column(Integer)
