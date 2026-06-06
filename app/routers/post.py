from .. import models, schemas
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..db import get_db
from typing import List
from ..oauth2 import get_current_user


router = APIRouter(
    prefix='/posts',
    tags=['posts']
)


# get
@router.get('/')
def get_posts(db: Session = Depends(get_db), response_model=List[schemas.Post]):
    return db.query(models.Post).all()

@router.get('/{id}', response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if post: return post
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='not found'
    )

# post
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# delete
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first():
        post.delete(synchronize_session=False)
        db.commit()
        return

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='not found'
    )

# update
@router.put('/{id}', response_model=schemas.Post)
def update_post(
    id: int, new_post: schemas.PostCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    if post_query.first():
        updated = post_query.update(new_post.model_dump(), synchronize_session=False)
        db.commit()
        return post_query.first()

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='not found'
    )