from typing import Optional
from uuid import uuid4
from pydantic import BaseModel, Field as DanticField
from sqlmodel import SQLModel, Field

class Task(SQLModel, table=True):
	id: str = Field(primary_key=True)
	name: str = Field(nullable=False, max_length=36)
	done: bool = Field(default=False)
	owner_id: str = Field(nullable=False, foreign_key="user.id")

class TaskRead(BaseModel):
	name: str = DanticField(max_length=36)
	done: bool = DanticField(default=False)

class TaskUpdate(BaseModel):
	name: Optional[str] = DanticField(max_length=36)
	done: Optional[bool] = DanticField(default=None)
