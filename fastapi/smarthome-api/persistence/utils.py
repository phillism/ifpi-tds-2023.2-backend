from sqlmodel import create_engine
from decouple import config

def obter_engine():
  db_url = config("DATABASE_URI")
  engine = create_engine(db_url, echo=True)
  
  return engine
