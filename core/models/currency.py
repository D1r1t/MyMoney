from base           import Base
from sqlalchemy.org import Mapped
from sqlalchemy.org import mapped_column
from sqlalchemy     import String

class Currency(Base.Base):
    __tablename__ = "currency"

    id: Mapped[int]       = mapped_column(primary_key=True)
    cur_name: Mapped[str] = mapped_column(Strign(150))
    is_main: Mapped[bool] = mapped_column(bool)

