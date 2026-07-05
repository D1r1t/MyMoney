from sqlalchemy.orm    import sessionmaker
from sqlalchemy        import select
from models.accounts   import Accounts
from models.categories import Categories
from models.moves      import Moves
from db.db             import engine
from datetime          import date, datetime

Session = sessionmaker(engine)

def create_new_move(
    plan_rec: bool, 
    rec_date: datetime, 
    account: Accounts, 
    move_is_income: bool, 
    category: Categories,
    move_sum: int,
    comment: str
) -> Moves: 

    with Session() as session:
        try: 

            new_move = Moves(plan_rec, rec_date, account, move_is_income, category, move_sum, comment)
            session.add(new_account)   
        except:
            session.rollback()
            raise
        else:
            session.commit()

