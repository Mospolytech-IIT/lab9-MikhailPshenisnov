from http.client import responses

from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse, FileResponse
import uvicorn
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://developer:developer@localhost:5432/BackendLab9_3DB"

engine = create_engine(SQLALCHEMY_DATABASE_URL)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    posts = relationship("Post", back_populates="user")


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship("User", back_populates="posts")


Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)

app = FastAPI()


@app.get("/create_user_form")
def create_user_form():
    return FileResponse(path="public/create_user_form.html")


@app.post("/create_user")
def create_user(username=Form(), email=Form(), password=Form()):
    try:
        session = Session()
        user = User(username=username, email=email, password=password)
        session.add(user)
        session.commit()
        response = JSONResponse(content={"message": "user created successfully"})
        session.close()
        return response
    except Exception as e:
        return JSONResponse(content={"message": str(e)})


@app.get("/read_user_form")
def read_user_form():
    return FileResponse(path="public/read_user_form.html")


@app.post("/read_user")
def read_user(id=Form()):
    try:
        session = Session()
        user = session.query(User).filter(User.id == id).first()
        response = JSONResponse(content={
            "user": f"id: {user.id}, username: {user.username}, email: {user.email}, password: {user.password}"})
        session.close()
        return response
    except Exception as e:
        return JSONResponse(content={"message": str(e)})


@app.get("/get_all_users")
def get_all_users():
    session = Session()
    users = session.query(User).all()
    result = [f"id: {user.id}, username: {user.username}, email: {user.email}, password: {user.password}"
              for user in users]
    session.close()
    return JSONResponse(content={"users": result})


@app.get("/update_user_form")
def update_user_form():
    return FileResponse(path="public/update_user_form.html")


@app.post("/update_user")
def update_user(id=Form(), new_username=Form(), new_email=Form(), new_password=Form()):
    try:
        session = Session()
        user = session.query(User).filter(User.id == id).first()
        user.username = new_username
        user.email = new_email
        user.password = new_password
        session.commit()
        response = JSONResponse(content={"message": "user updated successfully"})
        session.close()
        return response
    except Exception as e:
        return JSONResponse(content={"message": str(e)})


@app.get("/delete_user_form")
def delete_user_form():
    return FileResponse(path="public/delete_user_form.html")


@app.post("/delete_user")
def delete_user(id=Form()):
    try:
        session = Session()
        user = session.query(User).filter(User.id == id).first()
        session.query(Post).filter(Post.user_id == user.id).delete()
        session.delete(user)
        session.commit()
        response = JSONResponse(content={"message": "user deleted successfully"})
        session.close()
        return response
    except Exception as e:
        return JSONResponse(content={"message": str(e)})


@app.get("/create_post_form")
def create_post_form():
    return FileResponse(path="public/create_post_form.html")


@app.post("/create_post")
def create_post(title=Form(), content=Form(), user_id=Form()):
    try:
        session = Session()
        post = Post(title=title, content=content, user_id=user_id)
        session.add(post)
        session.commit()
        response = JSONResponse(content={"message": "post created successfully"})
        session.close()
        return response
    except Exception as e:
        return JSONResponse(content={"message": str(e)})


@app.get("/read_post_form")
def read_post_form():
    return FileResponse(path="public/read_post_form.html")


@app.post("/read_post")
def read_post(id=Form()):
    try:
        session = Session()
        post = session.query(Post).filter(Post.id == id).first()
        response = JSONResponse(
            content={"post": f"id: {post.id}, title: {post.title}, content: {post.content}, user_id: {post.user_id}"})
        session.close()
        return response
    except Exception as e:
        return JSONResponse(content={"message": str(e)})


@app.get("/get_all_posts")
def get_all_posts():
    session = Session()
    posts = session.query(Post).all()
    result = [f"id: {post.id}, title: {post.title}, content: {post.content}, user_id: {post.user_id}"
              for post in posts]
    session.close()
    return JSONResponse(content={"posts": result})


@app.get("/update_post_form")
def update_post_form():
    return FileResponse(path="public/update_post_form.html")


@app.post("/update_post")
def update_post(id=Form(), new_title=Form(), new_content=Form(), new_user_id=Form()):
    try:
        session = Session()
        post = session.query(Post).filter(Post.id == id).first()
        post.title = new_title
        post.content = new_content
        post.user_id = new_user_id
        session.commit()
        response = JSONResponse(content={"message": "post updated successfully"})
        session.close()
        return response
    except Exception as e:
        return JSONResponse(content={"message": str(e)})


@app.get("/delete_post_form")
def delete_post_form():
    return FileResponse(path="public/delete_post_form.html")


@app.post("/delete_post")
def delete_post(id=Form()):
    try:
        session = Session()
        post = session.query(Post).filter(Post.id == id).first()
        session.delete(post)
        session.commit()
        response = JSONResponse(content={"message": "post deleted successfully"})
        session.close()
        return response
    except Exception as e:
        return JSONResponse(content={"message": str(e)})


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
