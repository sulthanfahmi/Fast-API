from pydantic import BaseModel,EmailStr, Field
from datetime import datetime 
from typing import Optional
from enum import Enum
from fastapi import Query

class NameEnum(str,Enum):
    OPTION1 = "Virat"
    OPTION2 = "Dhoni"
    OPTION3 = "Rohit"

class PostBase(BaseModel):
    #Name: NameEnum  
    title : str
    content : str
    publish : bool = True
    #owner_id : int
    #rating : Optional[int] = None 

class CreatePost(PostBase):
    pass

class display(BaseModel):
    id : int
    email : EmailStr
    created_at : datetime

   
class Config:
     orm_mode = True

class Post(PostBase):
        id : int
        Name : str
        created_at : datetime
        owner_id : int
        owner : display
        
class Config:
    orm_mode = True

# For the table name user

class usercreate(BaseModel):
    email : EmailStr
    password : str

class updateUser(usercreate):
     pass


class User_Login(BaseModel):
     email : EmailStr
     password : str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
     id : Optional[int]  = None
    

class user(BaseModel):
     email : EmailStr

class VerifyEmail(BaseModel):
     email : str
     otp: str
     
     
     