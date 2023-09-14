from dotenv import dotenv_values, load_dotenv
from sqlmodel import create_engine

load_dotenv()
config = dotenv_values(".env")

def get_engine():
    db_url = 'sqlite:///database.db' if "DATABASE_URI" not in config else config["DATABASE_URI"]
    engine = create_engine(db_url, echo=True)

    return engine
