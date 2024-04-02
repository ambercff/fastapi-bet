from pydantic import BaseModel, validator
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Modelo usado para criar e dar update

class user(BaseModel):
    name: str
    username: str
    password: str
    balance: float
    token: str = None
    
    @validator('password')
    def valid_password(cls, value):
        
        passwordLen = list(value)
        
        if len(passwordLen) < 6:
            raise ValueError ("Your password must be at least 6 characters long!")
                
        return value
    
# Modelo para leitura
    
class userRead(BaseModel):
    id: int
    name: str
    username: str
    password: str
    balance: float
    token: str = None

class UserDB(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key = True)
    name = Column(String)
    username = Column(String)
    password = Column(String)
    balance = Column(Float)
    token = Column(String)
