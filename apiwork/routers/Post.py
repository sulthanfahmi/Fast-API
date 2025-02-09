from typing import List, Optional
from fastapi import  FastAPI,Response,status,HTTPException,Depends, APIRouter
from sqlalchemy.orm import Session 
from ..import models,schemas , oauth2 
from ..database import get_db
from ..schemas import NameEnum
from typing import List



router = APIRouter(
    prefix = "/profile",
    tags = ["Posts"]
)

my_posts = [{"title" : " favorite sports " , "content" : "Cricket" , "id" : 1},
                {"title" : "favorite food" , "content" : "pizza" , "id" : 2},
                {"title" : "favorite Movie" , "content" : "MsDhoni" , "id" : 3}]

# For the table name user 

#@router.get("/")
#def root():
 #   return {"message": "Welcome to my api !!"}


@router.get("/", response_model=List[schemas.Post])
def create_profile(db: Session = Depends(get_db),
                   current_user: schemas.user = Depends(oauth2.get_current_user),
                   limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    print(limit)  # Just for debugging
    
    # Filter posts by the current user's id
    posts = db.query(models.Post).filter(
        models.Post.owner_id == current_user.id,
        models.Post.title.contains(search)
    ).limit(limit).offset(skip).all()

    return posts


@router.get("/sqlalchemy")
def test_post(db: Session = Depends(get_db)):

    Connect_Database = db.query(models.Post).all()
    return  Connect_Database 


@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post(*, post: schemas.CreatePost, db: Session = Depends(get_db),
                current_user : int = Depends(oauth2.get_current_user),
                name : NameEnum):
    New_Post = post.dict()
    
    New_Post["Name"] = name.value
    
    # Check if 'owner_id' is provided in the post data, if not, set it to the current user's id
    if "owner_id" not in New_Post:
        New_Post["owner_id"] = current_user.id

    post = models.Post(**New_Post)

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform request action")
    
    db.add(post)
    db.commit()
    db.refresh(post)
    return post




 
@router.get("/latest")
def latest_post():

    post = my_posts[len(my_posts)-1]
    return{"Latest post" : post }

@router.get("/{id}", response_model = schemas.Post)
def create_profile(id : str,db: Session = Depends(get_db),
                   current_user : int = Depends(oauth2.get_current_user)):


    print(current_user)
    post = db.query(models.Post).filter(models.Post.id == id).first()
    print(post)

    if not post:
       raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                           detail =  f"the post with id: {id} not found")
       
    return post 


@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id : str, db: Session = Depends(get_db),
                current_user : int = Depends(oauth2.get_current_user)):

   
    print(current_user)

    post_query = db.query(models.Post).filter(models.Post.id == id)  

    post = post_query.first()


    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail =  f"The post with id : {id} does not exists")
        
    if post.owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                            detail = "Not authorized to perform request action")
    
    post_query.delete(synchronize_session = False)
        
    db.commit()
        
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}",response_model = schemas.Post)
def update_post(id : int , update_post:schemas.CreatePost , db : Session = Depends(get_db),
                current_user : int = Depends(oauth2.get_current_user)):
     
    
    print(current_user)
    update_query = db.query(models.Post).filter(models.Post.id == id)
    
    post=update_query.first()
    
    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail =  f"The post with id : {id} does not exists")
    
    if post.owner_id!= current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                            detail = "Not authorized to perform request action" )
    
    update_query.update(update_post.dict(),synchronize_session = False)
    db.commit()

    return update_query.first()
 