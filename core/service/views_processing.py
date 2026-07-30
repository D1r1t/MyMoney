from sqlalchemy.orm          import sessionmaker, joinedload
from sqlalchemy              import select, and_
from ..views.analitic_by_day import AnaliticByDay
from ..views.expenses_by_day import ExpensesByDay
from ..db.db                 import engine
from datetime                import date, datetime
from ..models.accounts       import Accounts
from ..models.categories     import Categories

# ================================================================================

Session = sessionmaker(engine)

# --------------------------------------------------------------------------------

def get_analitic_by_day(start_date: datetime, end_date: datetime) -> list[AnaliticByDay]: 
    with Session() as session:
        try: 
            statement  = select(AnaliticByDay).where(
                and_(
                    AnaliticByDay.rec_date >= start_date, 
                    AnaliticByDay.rec_date <= end_date
                )
            ).order_by(ExpensesByDay.rec_date)

            db_objects = session.scalars(statement).all()
            return db_objects  
        except:
            session.rollback()
            raise
        else:
            session.commit()

# --------------------------------------------------------------------------------

def get_expenses_by_day(start_date: datetime, end_date: datetime, acc: Account = None, cat: Category = None) -> list[ExpensesByDay]: 
    with Session() as session:
        statement  = select(ExpensesByDay).where(
            and_(
                ExpensesByDay.rec_date >= start_date, 
                ExpensesByDay.rec_date <= end_date
            )
        ).order_by(ExpensesByDay.rec_date)
        
        if acc is not None:
            statement = statement.where(ExpensesByDay.account_id == acc.id)

        if cat is not None:
            statement = statement.where(ExpensesByDay.category_id == cat.id)
        
        db_objects = session.scalars(
            statement.
                options(
                    joinedload(ExpensesByDay.account),
                    joinedload(ExpensesByDay.category)
                ) 
        ).all()
        return db_objects  



