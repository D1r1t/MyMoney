from sqlalchemy.orm          import sessionmaker
from sqlalchemy              import select, and_
from ..views.analitic_by_day import AnaliticByDay
from ..views.expenses_by_day import ExpensesByDay
from ..db.db                 import engine
from datetime                import date, datetime

Session = sessionmaker(engine)

def get_analitic_by_day(start_date: datetime, end_date: datetime) -> Array: 
    with Session() as session:
        try: 
            statement  = select(AnaliticByDay).where(and_(AnaliticByDay.rec_date >= start_date, AnaliticByDay.rec_date <= end_date))
            db_objects = session.scalars(statement).all()
            return db_objects  
        except:
            session.rollback()
            raise
        else:
            session.commit()

def get_expenses_by_day(start_date: datetime, end_date: datetime) -> Array: 
    with Session() as session:
        try: 
            statement  = select(ExpensesByDay).where(and_(ExpensesByDay.rec_date >= start_date, ExpensesByDay.rec_date <= end_date))
            db_objects = session.scalars(statement).all()
            return db_objects  
        except:
            session.rollback()
            raise
        else:
            session.commit()


