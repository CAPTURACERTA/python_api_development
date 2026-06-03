from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, Field
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from time import sleep


class Post(BaseModel):
    id: int = Field(
        default_factory=lambda: randrange(0,100000)
    )
    title: str
    content: str
    published: bool = True


app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='fastapi',
            user='postgres',
            password='...',                         #remove
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
def get_posts():
    cursor.execute(
        """
        SELECT * FROM posts
        """
    )
    return cursor.fetchall()

@app.get('/posts/{id}')
def get_post(id: int):
    cursor.execute(
        """
        SELECT * FROM posts
        WHERE id = %s
        """,(id,)
    )

    post = cursor.fetchone()
    if post: return post
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='not found'
    )

# post
@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute(
        """
        INSERT INTO posts
            (title, content, published)
        VALUES
            (%s, %s, %s)
        RETURNING *;
        """, (post.title, post.content, post.published)
    )
    conn.commit()
    return cursor.fetchone()


# delete
@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(
        """
        DELETE FROM posts
        WHERE id = %s
        RETURNING *;
        """, (id,)
    )
    
    if cursor.fetchone():
        conn.commit()
        return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='not found'
    )

# update
@app.put('/posts/{id}', )
def update_post(id: int, post: Post):
    cursor.execute(
        """
        UPDATE posts
        SET title = %s, content = %s, published = %s
        WHERE id = %s
        RETURNING *;
        """, (
            post.title, post.content, post.published, id
        )
    )
    
    if updated_post := cursor.fetchone():
        conn.commit()
        return updated_post
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='not found'
    )