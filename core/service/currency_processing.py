from sqlalchemy.orm    import sessionmaker
from sqlalchemy        import select
from models.currency   import Currency
from db.db             import engine

Session = sessionmaker(engine)

def create_new_currency(cur_name: str, is_main = False):
    with Session() as session:
        exists = get_currency(session, cur_name) is not None

        try:
            if exists:
                raise Exception

            new_currency = Currency(cur_name, is_main)
            session.add(new_currency)
        except:
            session.rollback()
            raise
        else:
            session.commit()

def get_currency(session, cur: int|str) -> Currency:
    if isinstance(cat, int):
        statement = select(Currency).where(Currency.id == cat)
    elif isinstance(cat, str):
        statement = select(Currency).where(Currency.cur_name == cat)

    db_object = session.scalars(statement).one_or_none()

    return db_object



