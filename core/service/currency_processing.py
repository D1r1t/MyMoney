from sqlalchemy.orm    import sessionmaker
from sqlalchemy        import select
from ..models.currency import Currency
from ..db.db           import engine
from ..exceptions      import CurrencyError, CurrencyMainAlreadyExistsError 

Session = sessionmaker(engine)

def create_new_currency(cur_name: str, is_main = False, change_main = False):
    with Session() as session:
        exists       = get_currency(session, cur_name) is not None
        current_main = is_main_currenсy_exists(session)

        try:
            if exists:
                raise CurrencyAlreadyExistsError(cur_name)

            if is_main: 
                if current_main != None and not change_main:
                    raise CurrencyMainAlreadyExistsError(current_main)
                else:
                    alter_main_to_comon(session, current_main)
            

            new_currency = Currency(cur_name, is_main)
            session.add(new_currency)
        except:
            session.rollback()
            raise
        else:
            session.commit()

def get_currency(session, cur: int|str) -> Currency:
    if isinstance(cur, int):
        statement = select(Currency).where(Currency.id == cur)
    elif isinstance(cur, str):
        statement = select(Currency).where(Currency.cur_name == cur)

    db_object = session.scalars(statement).one_or_none()

    return db_object

def is_main_currenсy_exists(session) -> Currency:
    statement = select(Currency).where(Currency.is_main == True)
    db_object = session.scalars(statement).one_or_none()
    return db_object

def alter_main_to_comon(session, currency: Currency):
    currency.is_main = False
    session.merege(currency)

def get_all_currencies() -> Array:
    with Session() as session:
        try:
            statement = select(Currency)
            db_object = session.scalars(statement).all()
        except:
            raise CurrencyError()
        else:
            return db_object
