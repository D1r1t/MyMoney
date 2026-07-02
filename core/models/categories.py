from base           import Base
from sqlalchemy.org import Mapped, mapped_column
from sqlalchemy     import String, ForeignKey

class Categories(Base.Base):
    __tablename__ = "categories"

    id: Mapped[int]       = mapped_column(primary_key=True)
    cat_name: Mapped[str] = mapped_column(String(150))