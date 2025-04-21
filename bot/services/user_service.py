from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    access_level = Column(Integer)

class UserService:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add_user(self, username, first_name, last_name, access_level):
        session = self.Session()
        new_user = User(username=username, first_name=first_name, last_name=last_name, access_level=access_level)
        session.add(new_user)
        session.commit()
        session.close()

    def get_user(self, username):
        session = self.Session()
        user = session.query(User).filter_by(username=username).first()
        session.close()
        return user

    def update_user_access(self, username, new_access_level):
        session = self.Session()
        user = session.query(User).filter_by(username=username).first()
        if user:
            user.access_level = new_access_level
            session.commit()
        session.close()

    def delete_user(self, username):
        session = self.Session()
        user = session.query(User).filter_by(username=username).first()
        if user:
            session.delete(user)
            session.commit()
        session.close()