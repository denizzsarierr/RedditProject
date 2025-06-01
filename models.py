from sqlalchemy import Column,Row,Integer,String,ForeignKey,create_engine,LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker


Base = declarative_base()

class User(Base):

    __tablename__ = "users"
    id = Column(Integer,primary_key=True)
    username = Column(String,unique=True)
    password = Column(String)
    profile_pic = Column(LargeBinary,nullable = False)
    posts = relationship("Post",back_populates="author")
    
    

class Post(Base):

    __tablename__ = "posts"
    id = Column(Integer,primary_key = True)
    title = Column(String(100))
    text = Column(String(1000))
    user_id = Column(Integer,ForeignKey("users.id"))
    author = relationship("User",back_populates='posts')
    


#Create database
engine = create_engine('sqlite:///redditproject.db')
# Create tables
Base.metadata.create_all(engine)
# Cursor
Session = sessionmaker(bind=engine)
