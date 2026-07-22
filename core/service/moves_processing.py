from sqlalchemy.orm      import sessionmaker, joinedload
from sqlalchemy          import select, and_
from ..models.accounts   import Accounts
from ..models.categories import Categories
from ..models.moves      import Moves
from ..db.db             import engine
from datetime            import date, datetime
from ..exceptions        import MovesError, MoveDoesntExists

Session = sessionmaker(engine)

def create_new_move(
    plan_rec: bool, 
    rec_date: datetime, 
    account: Accounts, 
    move_is_income: bool, 
    category: Categories,
    move_sum: int,
    comment: str = ""
): 

    with Session() as session:
        try: 
            new_move = Moves(plan_rec, rec_date, account, move_is_income, category, move_sum, comment)
            session.add(new_move)
        except:
            session.rollback()
            raise
        else:
            session.commit()

def update_move(
    id: int,
    plan_rec: bool, 
    rec_date: datetime, 
    account: Accounts, 
    move_is_income: bool, 
    category: Categories,
    move_sum: int,
    comment: str = ""
):
    with Session() as session:
        try: 
            move = get_move_by_id(session, id)

            if move == None:
                raise MoveDoesntExists(id)

            move.plan_rec       = plan_rec
            move.rec_date       = rec_date
            move.account        = account
            move.move_is_income = move_is_income
            move.category       = category
            move.move_sum       = move_sum
            move.comment        = comment
        except MoveDoesntExists:
            raise   
        except:
            session.rollback()
            raise
        else:
            session.commit()


def delete_move(id: int):
    with Session() as session:
        try:
            move = get_move_by_id(session, id)
            if move == None:
                raise MoveDoesntExists(id)
            
            session.delete(move)
        except MoveDoesntExists:
            raise MoveDoesntExists(id)
        except:
            session.rollback()
            raise
        else:
            session.commit() 

def get_moves(start_date: datetime, end_date: datetime) -> Array:
    with Session() as session:
        try:
            statement  = select(Moves).where(and_(Moves.rec_date >= start_date, Moves.rec_date <= end_date))
            db_objects = session.scalars(
                statement.
                options(
                    joinedload(Moves.account),
                    joinedload(Moves.category)
                )
            ).all()

            return db_objects
        except:
            session.rollback()
            raise
        else:
            session.commit()

def get_move_by_id(session, id: int) -> Moves | None:
    try:
        statement  = select(Moves).where(Moves.id == id)
        db_objects = session.scalars(statement).one_or_none()
        return db_objects
    except:
        session.rollback()
        raise
    else:
        session.commit()

