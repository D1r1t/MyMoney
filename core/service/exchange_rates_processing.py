from sqlalchemy.orm          import sessionmaker
from sqlalchemy              import select
from ..models.exchange_rates import Exchange_rates
from ..models.currency       import Currency
from ..db.db                 import engine
from datetime                import date, datetime

Session = sessionmaker(engine)

#возможно создание сессий будет перенесено в интерфейс или нужно будет подумать
#куда и как их правильно распределить
def create_new_exchange_rate(rate_date: datetime, main_currency: Currency, current_currency: Currency, rare: int) -> Exchange_rates: 
    with Session() as session:
        ex_rate = {"rate_date": rate_date, "main_currency": main_currency, "current_currency": current_currency, "rare": rare}

        #exists = get_exchange_rate(session, ex_rate) is not None

        try: 
            #if exists:
            #    raise Exception

            new_exchange_rate = Exchange_rates(ex_rate)
            session.add(new_account)   
        except:
            session.rollback()
            raise
        else:
            session.commit()

def get_exchange_rate(session, ex_rate: int | dict) -> Exchange_rates | None:
    if isinstance(ex_rate, int):
        statement = select(Exchange_rates).where(Exchange_rates.id == ex_rate)
    elif isinstance(ex_rate, dict): 
        statement = select(Exchange_rates).where(and_(Exchange_rates.main_currency == ex_rate["main_currency"], Exchange_rates.current_currency == ex_rate["current_currency"], Exchange_rates.rate_date == ex_rate["rate_date"]))

    db_object = session.scalars(statement).one_or_none()
    
    return db_object 