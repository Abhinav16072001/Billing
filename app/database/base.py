import yaml
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from app.models.customer import Customer  # Import the Customer model

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

Base.metadata.create_all(bind=engine)
