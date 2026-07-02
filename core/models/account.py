from base           import Base
from sqlalchemy.org import Mapped, mapped_column
from sqlalchemy     import String, ForeignKey

class Accounts(Base.Base):
    __tablename__ = "accounts"

    id: Mapped[int]       = mapped_column(primary_key=True)
    acc_name: Mapped[str] = mapped_column(String(150))
    currency: Mapped[int] = mapped_column(ForeignKey("Currency.id"))