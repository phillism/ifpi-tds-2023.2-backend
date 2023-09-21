from decouple import config
from sqlmodel import create_engine

def get_engine():
    db_url = config("DATABASE_URI")
    engine = create_engine(db_url, echo=True)

    return engine
