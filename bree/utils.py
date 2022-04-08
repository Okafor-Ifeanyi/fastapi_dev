from passlib.context import CryptContext
from .main import my_posts
pwd_content = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_content.hash(password)

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i