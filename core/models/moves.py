from .base               import Base
from sqlalchemy.orm      import Mapped, mapped_column, relationship
from sqlalchemy          import String, DateTime, Integer, ForeignKey
from datetime            import date, datetime
from typing              import Optional
from ..models.accounts   import Accounts
from ..models.categories import Categories


class Moves(Base):
    __tablename__ = "moves"

    id: Mapped[int]              = mapped_column(primary_key=True)
    plan_rec: Mapped[bool]       = mapped_column(default=False)
    rec_date: Mapped[datetime]   = mapped_column(DateTime)
    account_id: Mapped[int]      = mapped_column(ForeignKey("accounts.id"))
    move_is_income: Mapped[bool] = mapped_column(default=False)
    category_id: Mapped[int]     = mapped_column(ForeignKey("categories.id"))
    move_sum: Mapped[int]        = mapped_column(Integer)
    comment: Mapped[str]         = mapped_column(String(200))

    account: Mapped["Accounts"]    = relationship()
    category: Mapped["Categories"] = relationship()

    def __init__(self, 
                    plan_rec:       bool, 
                    rec_date:       datetime, 
                    account:        Accounts, 
                    move_is_income: bool, 
                    category:       Categories, 
                    move_sum:       int, 
                    comment:        str = ""
    ):
        self.plan_rec       = plan_rec
        self.rec_date       = rec_date
        self.account        = account
        self.move_is_income = move_is_income
        self.category       = category
        self.move_sum       = move_sum
        self.comment        = comment

    def __repr__(self) -> str:
        return (
            f"Move(id = {self.id}, plan_rec = {self.plan_rec}, rec_date = {self.rec_date}, )"
            f"account_id = {self.account_id}, move_is_income = {self.move_is_income}, category_id = {self.category_id}, "
            f"move_sum = {self.move_sum}, comment = {self.comment}"
        )