from jose import jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from ..environment.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRECT_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRECT_KEY, algorithm=ALGORITHM)

    return encoded_jwt