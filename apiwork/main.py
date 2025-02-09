from typing import Optional, List
from fastapi import  FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2 
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session 
from .import models, schemas, utils
from .database import engine,get_db
from .routers import Post,user,auth


 
models.Base.metadata.create_all(bind=engine) 

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host = "localhost" ,database = "fastapi" ,user = "postgres",
                            password = "Welcome@123", cursor_factory = RealDictCursor)
        cursor = conn.cursor()
        print("The Database was connected succesfully")
        break

    except Exception as error:
        print("The Database connection failed")
        print("Error", error)


   
my_posts = [{"title" : " favorite sports " , "content" : "Cricket" , "id" : 1},
                {"title" : "favorite food" , "content" : "pizza" , "id" : 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        
def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p["id"] == id:
            return i


 
app.include_router(Post.router)
app.include_router(user.router)
app.include_router(auth.routher)



