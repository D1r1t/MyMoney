from sqlalchemy import create_engine

db_url = "postgresql+psycopg2://postgres:2wsx@WSX@localhost:5432/my_money"

engine = create_engine(db_url, echo = True)

