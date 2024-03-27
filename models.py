from pydantic import BaseModel, validator
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# objeto pydantic é um modelo base 

# modelo pydantic para criar um objeto
class BetCreate(BaseModel):
    name: str
    odd: float
    price: float

    # Usamos o validator é usado para validar e processar dados antes que eles sejam atribuidos aos campos do model

    # Passamos a classe como parâmetro para 'esclarecer' que estamos nos referindo a própria classe
    @validator('price')
    def verification_price(cls, value):
        if value <= 0:
            raise ValueError('The price must be bigger than 0')
        return value
    
# Modelo pydantic para retornar os objetos
class BetRead(BaseModel):
    id: int
    name: str
    odd: float
    price: float

# Modelo pydantic para atualizar os objetos
class BetUpdate(BaseModel):
    name: str
    odd: float
    price: float

    @validator('price')
    def verification_price(cls, value):
        if value <= 0:
            raise ValueError('The price must be bigger than 0')
        return value

# Modelo SQLAlchemy, é usado para criar as tabelas no banco
class BetDB(Base):
    __tablename__ = 'bets'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    odd = Column(Float, index=True)
    price = Column(Float, index=True)