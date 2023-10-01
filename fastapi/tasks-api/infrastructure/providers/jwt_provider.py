from jose import jwt
from decouple import config

jwt_secret = config('JWT_SECRET')
jwt_alghorithm = config('JWT_ALGORITHM')

def encode(user_id: str):
    payload = { "id": user_id }
    encoded = jwt.encode(payload, jwt_secret, algorithm=jwt_alghorithm)

    return encoded

def decode(token: str):
    return jwt.decode(token, jwt_secret, algorithms=[jwt_alghorithm])
