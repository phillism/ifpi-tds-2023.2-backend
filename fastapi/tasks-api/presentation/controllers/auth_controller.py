from fastapi import APIRouter, Depends, HTTPException, status
from infrastructure.providers.auth_provider import handle_logged_user
from persistence.repositories.user_repository import UserRepository
import infrastructure.providers.hash_provider as hash_provider 
import infrastructure.providers.jwt_provider as jwt_provider

from presentation.models.user_model import User, UserInput, UserOutput

router = APIRouter(prefix='/auth', tags=['authorization'])
user_repository = UserRepository()

@router.post('/signup')
def signup(input: UserInput) -> UserOutput:
	user = User.from_user_input(input)
	created_user = user_repository.save(user)
	
	return UserOutput(
		id=created_user.id,
		username=created_user.username
	)

@router.post('/signin')
def signin(input: UserInput):
	user = user_repository.find_by_username(input.username)

	if user:
		password_matches = hash_provider.verify(input.password, user.password)

	if not user or not password_matches:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect password or invalid user.')
	
	token = jwt_provider.encode(str(user.id))
	return { "token": token }

@router.get('/me')
async def read_users_me(
    current_user: User = Depends(handle_logged_user)
):
    return UserOutput(**current_user.dict())
