from typing import Annotated
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from presentation.models.user_model import User
from persistence.repositories.user_repository import UserRepository

import infrastructure.providers.jwt_provider as jwt_provider

user_repository = UserRepository()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/signin')

def handle_logged_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
	credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

	try:
		payload = jwt_provider.decode(token)
		user_id = payload.get('id')
		found_user = user_repository.find_by_id(user_id)

		if not found_user:
			raise credentials_exception
		
		return found_user
	except JWTError:
		raise credentials_exception
	