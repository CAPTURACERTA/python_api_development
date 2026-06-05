from jose import JWTError, jwt
from datetime import datetime,timedelta, timezone
from .schemas import TokenData
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
SECRET_KEY = "goblins"
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_acess_token(token: str, credentials_exception):
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")

        if user_id:
            return TokenData(id=user_id)
        
        raise credentials_exception
    except JWTError:
        raise credentials_exception
    
def get_current_user(token: str = Depends(oauth2_scheme)):
    return verify_acess_token(
        token,
        HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="couldn't validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    )