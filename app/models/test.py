from typing import List, Optional
from pydantic import BaseModel, ValidationError, Field
from datetime import datetime

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
        from_attributes = True

# Test Schemas admin


class OptionSchema(BaseModel):
    id: int
    text: str
    is_correct: bool

    class Config:
        from_attributes = True
        from_attributes = True


class QuestionSchema(BaseModel):
    id: int
    text: str
    options: List[OptionSchema]

    class Config:
        from_attributes = True
        from_attributes = True


class TestSchema(BaseModel):
    id: int
    title: str
    description: str
    questions: List[QuestionSchema]

    class Config:
        from_attributes = True
        from_attributes = True

# Test Schemas User


class OptionWithoutCorrectness(BaseModel):
    id: int
    text: str

    class Config:
        from_attributes = True


class QuestionWithoutCorrectness(BaseModel):
    id: int
    text: str
    options: List[OptionWithoutCorrectness]

    class Config:
        from_attributes = True


class TestSchemaWithoutCorrectness(BaseModel):
    id: int
    title: str
    description: str
    questions: List[QuestionWithoutCorrectness]

    class Config:
        from_attributes = True


# Assign

class TestUserAssignment(BaseModel):
    user_id: List[int]
    test_id: List[int]
    start_time: datetime
    end_time: datetime
    duration: datetime = None
