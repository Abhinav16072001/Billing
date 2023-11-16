from typing import List
from pydantic import BaseModel, ValidationError, Field

# Create Test models


class OptionBase(BaseModel):
    text: str
    is_correct: bool


class QuestionBase(BaseModel):
    text: str
    options: List[OptionBase]


class TestCreate(BaseModel):
    title: str
    description: str
    questions: List[QuestionBase]


class TestBase(BaseModel):
    title: str
    description: str


class Test(TestBase):
    id: int

    class Config:
        orm_mode = True

# Test Schemas admin


class OptionSchema(BaseModel):
    id: int
    text: str
    is_correct: bool

    class Config:
        orm_mode = True
        from_attributes = True


class QuestionSchema(BaseModel):
    id: int
    text: str
    options: List[OptionSchema]

    class Config:
        orm_mode = True
        from_attributes = True


class TestSchema(BaseModel):
    id: int
    title: str
    description: str
    questions: List[QuestionSchema]

    class Config:
        orm_mode = True
        from_attributes = True

# Test Schemas User


class OptionWithoutCorrectness(BaseModel):
    id: int
    text: str

    class Config:
        orm_mode = True

class QuestionWithoutCorrectness(BaseModel):
    id: int
    text: str
    options: List[OptionWithoutCorrectness]

    class Config:
        orm_mode = True

class TestSchemaWithoutCorrectness(BaseModel):
    id: int
    title: str
    description: str
    questions: List[QuestionWithoutCorrectness]

    class Config:
        orm_mode = True