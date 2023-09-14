import datetime
from typing import List, Optional
import uuid
from pydantic import BaseModel
from sqlalchemy import JSON, Column
from sqlmodel import Field, SQLModel

class PersonInput(BaseModel):
    apelido: str = Field(max_length=32)
    nome: str = Field(max_length=100)
    nascimento: datetime.date
    stack: Optional[List[str]] = Field([], sa_column=Column(JSON)) # to see (implement stack name limit size using max_length)

class Person(SQLModel, PersonInput, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)