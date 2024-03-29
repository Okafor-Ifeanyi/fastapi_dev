from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.oauth2 import create_access_token
from app.config import settings 
from app.database import get_db 
from app.database import Base
from app import models
from alembic import command




SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Testing_SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)
 
 
# Dependency
def override_get_db():
    db = Testing_SessionLocal()
    try:
        yield db
    finally: 
        db.close()


@pytest.fixture()
def session():
    print("My session fixture ran")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = Testing_SessionLocal()
    try:
        yield db
    finally: 
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():

        try:
            yield session
        finally: 
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture
def test_user(client):
    user_data = {"email": "hello123@gmail.com", 
                    "password": "password123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201
    print(res.json())
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    access_token = create_access_token({"user_id": test_user['id'] })
    return access_token

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization" : f"Bearer {token}"
    }
    return client


@pytest.fixture
def test_user_2(client):
    user_data = {"email": "zeus@gmail.com", 
                    "password": "password123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201
    print(res.json())
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token_2(test_user_2):
    access_token = create_access_token({"user_id": test_user_2['id']})
    return access_token

@pytest.fixture
def authorized_client_2(client, token_2):
    client.headers = {
        **client.headers,
        "Authorization" : f"Bearer {token_2}"
    }
    return client


@pytest.fixture
def test_posts(test_user, session, test_user_2):
    posts_data = [{
        "title": "Checking out a post",
        "content": "Lets see how it goes",
        "owner_id": test_user['id']
    },{
        "title": "Checking out a 2nd post",
        "content": "See how it goes",
        "owner_id": test_user['id']
    }, {
        "title": "Checking out a 3rd post",
        "content": "How it goes",
        "owner_id": test_user['id']
    },{
        "title": "Checking out a 4th post",
        "content": "How it goes",
        "owner_id": test_user_2['id']
    }]

    def create_posts_model(post):
        return models.Post(**post)

    post_map = map(create_posts_model, posts_data)
    posts = list(post_map)


    session.add_all(posts)
    session.commit()

    posts = session.query(models.Post).all()
    return posts



