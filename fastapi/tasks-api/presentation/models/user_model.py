from uuid import UUID, uuid4
from pydantic import BaseModel, validator
from pydantic import Field as DanticField
from sqlmodel import Field, SQLModel
import infrastructure.providers.hash_provider as hash_provider

class User(SQLModel, table=True):
	id: str = Field(primary_key=True, default_factory=uuid4)
	username: str = Field(unique=True, nullable=False, max_length=16)
	password: str =  Field(nullable=False)

	@staticmethod
	def from_user_input(user_input: 'UserInput'):
		user_input_dict = user_input.dict()
		return User(
			**user_input_dict
		)
	
	@validator('password')
	def convert_password(cls, username):
		return hash_provider.hash(username)


class UserOutput(BaseModel):
	id: UUID
	username: str

class UserInput(BaseModel):
	username: str = DanticField(max_length=16)
	password: str =  DanticField(nullable=False)
