from fastapi import  Response,status,HTTPException,Depends, APIRouter
from sqlalchemy.orm import Session 
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import  database,schemas, models, utils , oauth2

routher = APIRouter(
    prefix = "/login",
    tags = ["Authentication"])

@routher.post("/", response_model = schemas.Token)
def login(user_creadentails : OAuth2PasswordRequestForm = Depends(),db: Session = Depends(database.get_db)):
#def login(user_creadentails : schemas.User_Login,db: Session = Depends(database.get_db)):

    user = db.query(models.user).filter(models.user.email == user_creadentails.username).first()

    if not user:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                            detail =  f"Invalid creadendetails")
    if not utils.verify(user_creadentails.password,user.password):
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                            detail =  f"Invalid creadendetails  verify password")
    
    access_token = oauth2.create_access_token(data={ "user_id" : user.id })
    
    return {"access_token" : access_token, "token_type" : "bearer" }



