from uuid import UUID
from fastapi import HTTPException
from sqlmodel import Session, select
from persistence.database import generate_engine
from presentation.models.task_model import Task, TaskUpdate


class TaskRepository:

	def __init__(self):
		self.session = Session(generate_engine())

	def find_by_id(self, task_id: str) -> Task:
		return self.session.get(Task, task_id)
	
	def find_by_user(self, user_id: str) -> list[Task]:
		if isinstance(user_id, UUID):
			user_id = str(user_id)
		
		sttm = select(Task).where(Task.owner_id == user_id)

		found_tasks = self.session.exec(sttm).fetchall()
		self.session.close()

		return found_tasks or []
	
	def save(self, task: Task) -> Task:
		self.session.add(task)
		self.session.commit()
		self.session.refresh(task)
		return task
	
	def update(self, task: Task, new_task: TaskUpdate) -> Task:
		for key, value in new_task.dict(exclude_unset=True).items():
			setattr(task, key, value)
		
		self.session.add(task)
		self.session.commit()
		self.session.refresh(task)
		self.session.close()

		return task
	
	def delete(self, task_id: str):
		found_task = self.session.get(Task, task_id)

		if not found_task:
			raise HTTPException(400, 'Task not found')

		self.session.delete(found_task)
		self.session.commit()
		self.session.close()
		return True
	