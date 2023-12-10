import yaml
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Boolean, Column, Integer, ForeignKey, String, DateTime, Table, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

with open('app/utility/config.yml', 'r') as file:
    yaml_data = yaml.load(file, Loader=yaml.FullLoader)

DATABASE_URL = yaml_data['mysql']['url']

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Define the association table for user-test assignments
user_test_association = Table(
    'user_test_assignment', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('test_id', Integer, ForeignKey('tests.id')),
    Column('start_time', String(10)),
    Column('end_time', String(10)),
    Column('duration', String(10)),
    Column('is_expired', Boolean),
    Column('created_at', DateTime, default=func.now()),
    Column('updated_at', DateTime, default=func.now(), onupdate=func.now())
)


class Customerdb(Base):
    __tablename__ = "customer"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    email = Column(String(50))


class Userdb(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50))
    name = Column(String(50))
    hashed_password = Column(String(100))
    role = Column(String(10))
    disabled = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, onupdate=func.now(),
                        default=func.now(), nullable=False)

    tests = relationship(
        "Test", secondary=user_test_association, back_populates="users")


class Test(Base):
    __tablename__ = "tests"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    description = Column(String(255))

    questions = relationship("Question", back_populates="test")
    users = relationship(
        "Userdb", secondary=user_test_association, back_populates="tests")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(255))
    test_id = Column(Integer, ForeignKey("tests.id"))

    test = relationship("Test", back_populates="questions")

    options = relationship("Option", back_populates="question")


class Option(Base):
    __tablename__ = "options"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(255))
    is_correct = Column(Boolean, default=False)
    question_id = Column(Integer, ForeignKey("questions.id"))

    question = relationship("Question", back_populates="options")

# menu


class MenuItemDb(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    price = Column(Float, nullable=False)
    image_url = Column(String(255))
    category = Column(String(100), nullable=False)
    # Establishing the user relationship
    user_id = Column(Integer, ForeignKey('users.id'))


Base.metadata.create_all(bind=engine)
