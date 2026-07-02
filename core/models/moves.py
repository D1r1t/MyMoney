from base           import Base
from sqlalchemy.org import Mapped, mapped_column
from sqlalchemy     import String, DateTime, Integer, ForeignKey
from datetime       import date, datetime

class Moves(Base.Base):
    __tablename__ = "moves"

    id: Mapped[int] = mapped_column(primary_key=True)
    plan_rec: Mapped[bool] = mapped_column(bool)
    rec_date: Mapped[datetime] = mapped_column(DateTime)
    account: Mapped[int] = mapped_column(ForeignKey("Accounts.id"))
    move_is_income: Mapped[bool] = mapped_column(bool)
    category: Mapped[int] = mapped_column(ForeignKey("Categories.id"))
    move_sum: Mapped[int] = mapped_column(Integer)
    comment: Mapped[str] = mapped_column(Strign(200))