from importlib import import_module
from statistics import mode
from fastapi import APIRouter, Response, status, HTTPException, Depends
from app import oauth2
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from typing import List, Optional

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model= List[schemas.PostOut])
# @router.get("/")
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), 
limit: int = 10, skip: int = 0, search: Optional[str]=""):
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    # print(limit)

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("Votes")).join( 
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
        models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.PostResponse)
def create_posts(post: schemas.PostCreate , db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts(title, content, published) 
    #                 VALUES(%s, %s, %s) RETURNING * """,
    #                 (post.title, post.content, post.published))
    # new_post = cursor.fetchone() 

    # conn.commit()
    print(current_user.id)
    # print(current_user.email)
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post
 
 
# @app.get("/posts/latest")
# def get_latest_post():
#     post = my_posts[len(my_posts)-1 ]
#     print(post)
#     return post


@router.get("/{id}", response_model= schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s;""", (str(id),))
    # post = cursor.fetchone()
    print(current_user)

    post = db.query(models.Post, func.count(models.Vote.post_id).label("Votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                    detail = f"Post with id: {id} was not found")

    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
    #     detail="Not authorized to perform requested action")

    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
      
    # cursor.execute(
    #     """DELETE FROM posts WHERE id = %s returning *""", (str(id),)) 
    # deleted_post = cursor.fetchone()
    # conn.commit()
    print(current_user)
    deleted_post_query = db.query(models.Post).filter(models.Post.id == id)
    
    deleted = deleted_post_query.first()

    if deleted == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail = f"Post with id: {id} was not found")

    if deleted.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
        detail="Not authorized to perform requested action")

    deleted_post_query.delete(synchronize_session=False)
    db.commit()
        
    return Response(status_code=status.HTTP_204_NO_CONTENT)
   

@router.put("/{id}", response_model= schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate , db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute( 
    #     """UPDATE posts SET title = %s, content = %s, published = %s WHERE ID = %s RETURNING *""",
    #     (post.title, post.content, post.published, str),)
    # updated_post = cursor.fetchone()
    # conn.commit()
    print(current_user)
    post_query = db.query(models.Post).filter(models.Post.id == id)

    updated_post = post_query.first()

    if updated_post == None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                    detail = f"Post with id: {id} was not found")

    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
        detail="Not authorized to perform requested action")


    post_query.update(post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()