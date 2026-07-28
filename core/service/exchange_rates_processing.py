from sqlalchemy.orm          import sessionmaker, joinedload
from sqlalchemy              import select, and_
from ..models.exchange_rates import ExchangeRates
from ..models.currency       import Currency
from ..db.db                 import engine
from datetime                import date, datetime

# ================================================================================

Session = sessionmaker(engine)

# --------------------------------------------------------------------------------

def create_new_exchange_rate(rate_date: datetime, main_currency: Currency, current_currency: Currency, rare: int) -> Exchange_rates: 
    with Session() as session:
        ex_rate = {"rate_date": rate_date, "main_currency": main_currency, "current_currency": current_currency, "rare": rare}

        #exists = get_exchange_rate(session, ex_rate) is not None

        try: 
            #if exists:
            #    raise Exception

            new_exchange_rate = ExchangeRates(rate_date, main_currency, current_currency, rare)
            session.add(new_exchange_rate)   
        except:
            session.rollback()
            raise
        else:
            session.commit()

# --------------------------------------------------------------------------------

def get_exchange_rate(session, ex_rate: int | dict) -> ExchangeRates | None:
    if isinstance(ex_rate, int):
        statement = select(ExchangeRates).where(ExchangeRates.id == ex_rate)
    elif isinstance(ex_rate, dict): 
        statement = select(ExchangeRates).where(and_(ExchangeRates.main_currency == ex_rate["main_currency"], Exchange_rates.current_currency == ex_rate["current_currency"], Exchange_rates.rate_date == ex_rate["rate_date"]))

    db_object = session.scalars(statement).one_or_none()
    
    return db_object 

# --------------------------------------------------------------------------------

def get_all_rates(start_date: datetime, end_date: datetime) -> list[ExchangeRates]:
    with Session() as session:
        try:
            statement  = select(ExchangeRates).where(and_(ExchangeRates.rate_date >= start_date, ExchangeRates.rate_date <= end_date)).order_by(ExchangeRates.rate_date)
            db_objects = session.scalars(
                statement.
                options(
                    joinedload(ExchangeRates.main_currency),
                    joinedload(ExchangeRates.current_currency)
                )
            ).all()

            return db_objects
        except:
            session.rollback()
            raise
        else:
            session.commit()

