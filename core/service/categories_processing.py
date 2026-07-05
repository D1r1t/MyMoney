from sqlalchemy.orm    import sessionmaker
from sqlalchemy        import select
from models.categories import Categories
from db.db             import engine

Session = sessionmaker(engine)

def create_new_category(cat_name: str):
    with Session() as session:
        exists = get_category(session, cat_name) is not None

        try:
            if exists:
                raise Exception

            new_category = Categories(cat_name)
            session.add(new_category)
        except:
            session.rollback()
            raise
        else:
            session.commit()

def get_category(session, cat: int|str) -> Categories:
    if isinstance(cat, int):
        statement = select(Categories).where(Categories.id == cat)
    elif isinstance(cat, str):
        statement = select(Categories).where(Categories.cat_name == cat)

    db_object = session.scalars(statement).one_or_none()

    return db_object



