from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, Field
from random import randrange


class Post(BaseModel):
    id: int = Field(
        default_factory=lambda: randrange(0,100000)
    )
    title: str
    content: str
    published: bool = True


all_posts = [
    Post(id=1, title='dogs', content='3 cried')
]


app = FastAPI()


# get
@app.get('/posts')
def get_posts():
    return all_posts

@app.get('/posts/{id}')
def get_post(id: int):
    for post in all_posts:
        if post.id == int(id): return post

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='not found'
    )

# post
@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    all_posts.append(post)
    return {'data': post}


# delete
@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post_index = None
    for index, post in enumerate(all_posts):
        if post.id == int(id):
            post_index = index
            break
    
    if post_index:
        del all_posts[post_index]
        return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='not found'
    )

# update
@app.put('/posts/{id}', )
def update_post(id: int, post: Post):
    post_index = None
    for index, p in enumerate(all_posts):
        if p.id == int(id):
            post_index = index
            break
    
    if post_index is not None:
        post.id = all_posts[post_index].id
        all_posts[post_index] = post
        print(all_posts)
        return
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='not found'
    )