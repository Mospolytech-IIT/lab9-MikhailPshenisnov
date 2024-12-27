from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker


def db_manip():
    SQLALCHEMY_DATABASE_URL = "postgresql://developer:developer@localhost:5432/BackendLab9DB"

    engine = create_engine(SQLALCHEMY_DATABASE_URL)

    # Создание модели данных
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

    # Создание таблиц
    Base.metadata.create_all(bind=engine)

    # Заполнение бд данными
    Session = sessionmaker(bind=engine)
    session = Session()

    user1 = User(username="Oleg", email="Oleg@yandex.ru", password="password")
    user2 = User(username="Ivan", email="Ivan@gmail.com", password="qwerty")
    user3 = User(username="Dima", email="Dima@outlook.com", password="12345678")
    user4 = User(username="Petr", email="Petr@mail.ru", password="0000")
    user5 = User(username="Kate", email="Kate@yahoo.com", password="111111111")

    session.add_all([user1, user2, user3, user4, user5])
    session.commit()

    post1 = Post(title="First Post", content="First post.", user_id=user1.id)
    post2 = Post(title="Second Post", content="Another post.", user_id=user1.id)
    post3 = Post(title="Hello", content="Hello, World!", user_id=user2.id)
    post4 = Post(title="Numbers", content="1, 2, 3, 4, 5, 6, 7, 8, 9, 10.", user_id=user3.id)
    post5 = Post(title="Post", content="Post text.", user_id=user5.id)

    session.add_all([post1, post2, post3, post4, post5])
    session.commit()

    # Считывание данных
    users = session.query(User).all()
    for user in users:
        print(f"id: {user.id}, username: {user.username}, email: {user.email}, password: {user.password}")
    print()

    posts = session.query(Post).join(User).all()
    for post in posts:
        print(f"id: {post.id}, title: {post.title}, content: {post.content}, user_id: {post.user_id}\n"
              f"author - id: {post.user.id}, username: {post.user.username}, email: {post.user.email}, password: "
              f"{post.user.password}")
    print()

    user_posts = session.query(Post).filter(Post.user_id == user1.id).all()
    for post in user_posts:
        print(f"title: {post.title}, content: {post.content}")
    print()

    # Обновление данных
    user_to_update = session.query(User).filter(User.id == user4.id).first()
    print(f"id: {user_to_update.id}, username: {user_to_update.username}, email: {user_to_update.email}, password: "
          f"{user_to_update.password}")
    if user_to_update:
        user_to_update.email = "Petr@yandex.ru"
        session.commit()
    session.refresh(user_to_update)
    print(f"id: {user_to_update.id}, username: {user_to_update.username}, email: {user_to_update.email}, password: "
          f"{user_to_update.password}")
    print()

    post_to_update = session.query(Post).filter(Post.id == post1.id).first()
    print(f"id: {post_to_update.id}, title: {post_to_update.title}, content: {post_to_update.content}, user_id: "
          f"{post_to_update.user_id}")
    if post_to_update:
        post_to_update.content += " new text"
        session.commit()
    session.refresh(post_to_update)
    print(f"id: {post_to_update.id}, title: {post_to_update.title}, content: {post_to_update.content}, user_id: "
          f"{post_to_update.user_id}")
    print()

    # Удаление данных
    posts = session.query(Post).join(User).all()
    for post in posts:
        print(f"id: {post.id}, title: {post.title}, content: {post.content}, user_id: {post.user_id}\n"
              f"author - id: {post.user.id}, username: {post.user.username}, email: {post.user.email}, password: "
              f"{post.user.password}")
    print()
    post_to_delete = session.query(Post).filter(Post.id == post3.id).first()
    if post_to_delete:
        session.delete(post_to_delete)
        session.commit()
    posts = session.query(Post).join(User).all()
    for post in posts:
        print(f"id: {post.id}, title: {post.title}, content: {post.content}, user_id: {post.user_id}\n"
              f"author - id: {post.user.id}, username: {post.user.username}, email: {post.user.email}, password: "
              f"{post.user.password}")
    print()

    users = session.query(User).all()
    for user in users:
        print(f"id: {user.id}, username: {user.username}, email: {user.email}, password: {user.password}")
    user_posts = session.query(Post).filter(Post.user_id == user1.id).all()
    for post in user_posts:
        print(f"title: {post.title}, content: {post.content}")
    print()
    user_to_delete = session.query(User).filter(User.id == user1.id).first()
    if user_to_delete:
        session.query(Post).filter(Post.user_id == user_to_delete.id).delete()
        session.delete(user_to_delete)
        session.commit()
    users = session.query(User).all()
    for user in users:
        print(f"id: {user.id}, username: {user.username}, email: {user.email}, password: {user.password}")
    user_posts = session.query(Post).filter(Post.user_id == user1.id).all()
    for post in user_posts:
        print(f"title: {post.title}, content: {post.content}")
    print()


if __name__ == '__main__':
    db_manip()
