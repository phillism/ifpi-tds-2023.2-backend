from sqlmodel import create_engine

def get_engine():
    db_url = 'sqlite:///database9.db'
    engine = create_engine(db_url, echo=True)

    return engine
 