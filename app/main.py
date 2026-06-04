from fastapi import FastAPI, status, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
from time import sleep
from . import models
from .db import engine, get_db
from .schemas import PostCreate
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='fastapi',
            user='postgres',
            password='fastapiproject',
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print('Succesfully connected to db')
        break
    except Exception as e:
        print('failed to connect to db:',e)
        sleep(2)


# get
@app.get('/posts')
def get_posts(db: Session = Depends(get_db)):
    return db.query(models.Post).all()

@app.get('/posts/{id}')
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if post: return post
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='not found'
    )

# post
@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_posts(post: PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# delete
@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
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
@app.put('/posts/{id}', )
def update_post(id: int, new_post: PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    if post_query.first():
        updated = post_query.update(new_post.model_dump(), synchronize_session=False)
        db.commit()
        return post_query.first()

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='not found'
    )