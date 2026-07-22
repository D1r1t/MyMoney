from .base          import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy     import String


class Currency(Base):
    __tablename__ = "currency"

    id: Mapped[int]       = mapped_column(primary_key=True)
    cur_name: Mapped[str] = mapped_column(String(150))
    is_main: Mapped[bool] = mapped_column(default=False)

    def __init__(self, cur_name: str, is_main: bool):
        self.cur_name = cur_name
        self.is_main  = is_main

    def __repr__(self) -> str:
        return f"Currency(if = {self.id}, cur_name = {self.cur_name}, is_main = {self.is_main})"
