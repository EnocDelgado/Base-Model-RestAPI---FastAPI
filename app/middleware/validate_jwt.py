from jose import JWTError, jwt
from ..schemas import user
from fastapi.security import OAuth2PasswordBearer
from ..environment.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRECT_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRECT_KEY, algorithms=ALGORITHM)

        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        
        token_data = user.TokenData(id=str(id))

    except JWTError:
        raise credentials_exception
    
    return token_data