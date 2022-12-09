from pydantic import BaseModel, Field, EmailStr
from sqlmodel import SQLModel
from typing import Optional

class UserSchema(BaseModel):
    fullname : str = Field(...)
    username : str = Field(...)
    password : str = Field(...)
    
    class Config:
        the_schema = {
            "example" : {
                "fullname": "Ryu",
                "username": "SeRyuu",
                "password": "pass"
            }
        }

class UserLoginSchema(BaseModel):
    username : str = Field(...)
    password : str = Field(...)
    
    class Config:
        the_schema = {
            "example" : {
                "username": "SeRyuu",
                "password": "pass"
            }
        }

class DataAntrian(BaseModel):
    id: int = Field(...)
    patient: str = Field(...)
    sudah_masuk: bool = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "patient": "Nama",
                "sudah_masuk": "false"
            }
        }