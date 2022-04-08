import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .database import engine, get_db
from fastapi import FastAPI, Response, status, HTTPException, Depends
from . import models, schemas
from sqlalchemy.orm import Session
from typing import List
from .izu import user



models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# FASTAPI_PW = os.environ['FASTAPI_PASSWORD']

while True:


    try:
        conn = psycopg2.connect(host= 'localhost', database= 'fastapi', user= 'postgres',
                                password= 'Ifeanyi058', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successfull") 
        break

    except Exception as error:
        print("connecting to database failed")
        print("Error: ", error)
        time.sleep(2)

my_posts = [ {"title": "title of post 1", "content": "content of post 1", "id": 1}, 
            {"title": "Favorite food  2", "content": "I like pizza", "id": 2}   
         ]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i



@app.get("/")
def root():
    return {"message": "Welcome to my api"} 

# app.include_router(user.router)


@app.get("/", response_model= List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()

    posts = db.query(models.Posts).all()
    return posts


@app.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.PostResponse)
def create_posts(post: schemas.PostCreate , db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts(title, content, published) 
    #                 VALUES(%s, %s, %s) RETURNING * """,
    #                 (post.title, post.content, post.published))
    # new_post = cursor.fetchone() 

    # conn.commit()
    new_post = models.Posts(**post.dict())
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post
 
 
# @app.get("/posts/latest")
# def get_latest_post():
#     post = my_posts[len(my_posts)-1 ]
#     print(post)
#     return post


@app.get("/{id}", response_model= schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s;""", (str(id),))
    # post = cursor.fetchone()
    
    post = db.query(models.Posts).filter(models.Posts.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                    detail = f"Post with id: {id} was not found")
    return post

@app.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
     
    # cursor.execute(
    #     """DELETE FROM posts WHERE id = %s returning *""", (str(id),)) 
    # deleted_post = cursor.fetchone()
    # conn.commit()
    deleted_post = db.query(models.Posts).filter(models.Posts.id == id)

    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail = f"Post with id: {id} was not found")

    deleted_post.delete(synchronize_session=False)
    db.commit()
        
    return Response(status_code=status.HTTP_204_NO_CONTENT)
   

@app.put("/{id}", response_model= schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate , db: Session = Depends(get_db)):

    # cursor.execute( 
    #     """UPDATE posts SET title = %s, content = %s, published = %s WHERE ID = %s RETURNING *""",
    #     (post.title, post.content, post.published, str),)
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Posts).filter(models.Posts.id == id)

    updated_post = post_query.first()

    if updated_post == None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                    detail = f"Post with id: {id} was not found")

    post_query.update(post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()