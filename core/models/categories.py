from base           import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy     import String, ForeignKey

class Categories(Base):
    __tablename__ = "categories"

    id: Mapped[int]       = mapped_column(primary_key=True)
    cat_name: Mapped[str] = mapped_column(String(150))

    def __init__(self, cat_name: str):
        self.cat_name = cat_name

    def __repr__(sefl) -> str:
        return f"Categories(id = {self.id}, cat_name = {self.cat_name})"
