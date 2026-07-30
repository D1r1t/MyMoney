from ..models.base     import Base
from sqlalchemy.orm    import Mapped, mapped_column, relationship
from sqlalchemy        import String, ForeignKey, Integer
from ..models.currency import Currency
from datetime          import datetime

# ================================================================================

class ExpensesByDay(Base):
    __tablename__ = "expenses_by_day"

    rec_date:    Mapped[datetime]         = mapped_column(primary_key=True)
    account_id:  Mapped[int]              = mapped_column(ForeignKey("accounts.id"))
    category_id: Mapped[int]              = mapped_column(ForeignKey("categories.id"))
    expense:     Mapped[Integer]          = mapped_column(Integer)

    account: Mapped["Accounts"]    = relationship()
    category: Mapped["Categories"] = relationship()
