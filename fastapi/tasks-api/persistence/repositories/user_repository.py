from uuid import uuid4
from fastapi import HTTPException
from sqlmodel import Session, select
from persistence.database import generate_engine
from presentation.models.user_model import User


class UserRepository:

	def __init__(self):
		self.session = Session(generate_engine())

	def find_by_id(self, user_id: str) -> User:
		return self.session.get(User, user_id)
	
	def find_by_username(self, username: str):
		sttm = select(User).where(User.username == username)
		found_user = self.session.exec(sttm).first()
		self.session.close()

		return found_user

	def save(self, user: User):
		user.id = str(uuid4())
		if self.find_by_username(user.username):
			raise HTTPException(400, 'User with this username already exists.')
		
		self.session.add(user)
		self.session.commit()
		self.session.refresh(user)
		return user
	