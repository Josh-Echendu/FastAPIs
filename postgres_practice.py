from typing import Optional
from fastapi import Body, FastAPI, HTTPException, Response, status
from pydantic import BaseModel
from psycopg2.extras import RealDictCursor
import psycopg2
import time


app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
                                password='qwerty12345', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection successfull")
        break
    except Exception as e:
        print("connection Failed: ", e)
        time.sleep(2)


@app.get('/posts')
def get_post():
    cursor.execute("""SELECT * FROM post""")
    posts = cursor.fetchall()
    return {"post": posts}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    posts = post.model_dump()
    cursor.execute("""INSERT INTO post (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
                   (posts.get('title'), posts.get('content'), posts.get('published')))
    result = cursor.fetchone()
    conn.commit()
    return {"data": result}



@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM post WHERE id = (%s)""", (str(id),))
    result = cursor.fetchone()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    return {"data": result}



@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM post WHERE id = %s RETURNING *""", (str(id),))
    result = cursor.fetchone()
    conn.commit()
    if result == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    posts = post.model_dump()
    cursor.execute("""UPDATE post SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", 
                  (posts.get('title'), posts.get('content'), posts.get('published'), str(id),))
    result = cursor.fetchone()
    conn.commit()

    if result == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    return {'data': result}