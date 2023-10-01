from sqlmodel import create_engine, SQLModel
from decouple import config


def generate_engine():
    database_uri = config('DATABASE_URI')

    engine = create_engine(database_uri, echo=True)
    return engine


def load_tables():
    engine = generate_engine()

    import presentation.models.task_model
    SQLModel.metadata.create_all(engine)
