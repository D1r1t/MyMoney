from sqlalchemy.orm  import sessionmaker
from sqlalchemy      import select
from models.accounts import Accounts
from models.currency import Currency
from db.db           import engine

Session = sessionmaker(engine)

#возможно создание сессий будет перенесено в интерфейс или нужно будет подумать
#куда и как их правильно распределить
def create_new_account(acc_name: str, currency: Currency) -> Accounts: 
    with Session() as session:
        exists = get_account(session, acc_name) is not None

        try: 
            if exists:
                raise Exception

            new_account = Accounts(acc_name, currency)
            session.add(new_account)   
        except:
            session.rollback()
            raise
        else:
            session.commit()

def get_account(session, acc: int | str) -> Accounts | None:
    if isinstance(acc, int):
        statement = select(Accounts).where(Accounts.id == acc)
    elif isinstance(acc, str):
        statement = select(Accounts).where(Accounts.acc_name == acc)

    db_object = session.scalars(statement).one_or_none()
    
    return db_object 