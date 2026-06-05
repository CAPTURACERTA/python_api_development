from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..db import get_db
from ..schemas import UserLogin
from ..models import User
from ..utils import verify
from ..oauth2 import create_access_token


router = APIRouter(
    tags=['Authentication']
)

@router.post('/login')
def login(
    credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == credentials.username).first()

    if user and verify(credentials.password, user.password):
        access_token = create_access_token(
            data = {'user_id': user.id}
        )
        return {
            'acess_token': access_token,
            'token_type': 'bearer'
        }
        

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='Invalid Credentials'
    )