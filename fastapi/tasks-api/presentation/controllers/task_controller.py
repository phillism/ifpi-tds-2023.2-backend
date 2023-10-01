from fastapi import APIRouter, Depends, HTTPException, status
from persistence.repositories.task_repository import TaskRepository
from presentation.models.task_model import Task, TaskRead, TaskUpdate

from presentation.models.user_model import User
from infrastructure.providers.auth_provider import handle_logged_user

router = APIRouter(prefix='/tasks', tags=['tasks'])
task_repository = TaskRepository()

@router.get('/')
def list_tasks(current_user: User = Depends(handle_logged_user)):
	found_tasks = task_repository.find_by_user(current_user.id)
	return found_tasks

@router.post('/')
def add_tasks(task: TaskRead, current_user: User = Depends(handle_logged_user)):
	created_task = task_repository.save(Task(**task.dict(), owner_id=current_user.id))

	return created_task

@router.put('/{task_id}')
def update_task(new_task: TaskUpdate | None, task_id: str, current_user: User = Depends(handle_logged_user)):
	if all(value is None for value in new_task.dict().values()):
		return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You need to pass an valid object.")

	found_task = task_repository.find_by_id(task_id)
	
	if not found_task or found_task.owner_id != str(current_user.id):
		raise HTTPException(status_code=404, detail='Task not found')
	
	updated_task = task_repository.update(found_task, new_task)
	return updated_task

@router.delete('/{task_id}', status_code=204)
def delete_task(task_id: str, current_user: User = Depends(handle_logged_user)):
	found_task = task_repository.find_by_id(task_id)
	
	if not found_task or found_task.owner_id != str(current_user.id):
		raise HTTPException(status_code=404, detail='Task not found')
	
	task_repository.delete(task_id)
