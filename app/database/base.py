import yaml
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

with open('config.yml', 'r') as file:
    yaml_data = yaml.load(file, Loader=yaml.FullLoader)

DATABASE_URL = yaml_data['mysql']['url']

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Customerdb(Base):
    __tablename__ = "customer"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    email = Column(String(50))


class Userdb(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50))
    full_name = Column(String(50))
    email = Column(String(50))
    hashed_password = Column(String(100))
    disabled = False
    created_at = Column(DateTime, server_default=func.now(), nullable=False)


Base.metadata.create_all(bind=engine)
