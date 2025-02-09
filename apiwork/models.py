from sqlalchemy import Column, Integer, String, Boolean, func, ForeignKey, Enum
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from .database import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .schemas import NameEnum
 

class Post(Base):
    __tablename__ = "Post"

    id = Column(Integer, primary_key = True, nullable = False) 
    Name = Column(String, nullable = False)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    publish = Column(Boolean, nullable = False ,server_default = "True")
    created_at = Column(TIMESTAMP(timezone = True),server_default = func.now() ,nullable = False)
    owner_id = Column(Integer, ForeignKey("user.id" , ondelete = "CASCADE"),nullable = False) 
    owner = relationship("user")

class user(Base):
    __tablename__= "user"

    id = Column(Integer, primary_key = True, nullable = False)
    email = Column(String, unique = True, nullable = False )
    password = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone = True),server_default = func.now(),onupdate = func.now() ,nullable = False)
    otp  =  Column(String)
