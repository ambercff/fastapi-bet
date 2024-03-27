from fastapi import FastAPI, HTTPException, Response, status, Depends
from sqlalchemy.orm import Session
from database import *
from models import *
from typing import List
import requests

app = FastAPI()

tokens = []

# 'response_model' serve para dizer qual tipo de retorno a função vai ter, nesse caso vai ser o tipo ItemRead, um modelo criado no arquivo models.py
@app.post('/create_bet', response_model=BetRead)
async def create_bet(item: BetCreate, db: Session = Depends(get_db)):
    exists = db.query(BetDB).filter(BetDB.name == item.name).first()

    if exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="name is already created")
    # Converte o pydantic para um dicionario
    db_item = BetDB(**item.model_dump())
    # Adiciona a sessao do banco de dados
    db.add(db_item)
     # Atualiza o ItemDB com os valores do banco após o commit, gerando um novo id
    db.commit()

    return db_item

@app.get('/bets', response_model=List[BetRead])
async def get_all_bets(db: Session = Depends(get_db)):
    db_items = db.query(BetDB).all()

    if len(db_items) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There are no bets registered")
    
    return db_items

@app.get('/bets/{bet_id}', response_model=BetRead)
async def get_bet(bet_id: int, db: Session = Depends(get_db)):
    db_item = db.query(BetDB).filter(BetDB.id == bet_id).first()

    if db_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bet not found")
    
    return db_item

@app.put('/bets/{bet_id}', response_model=BetRead)
async def update_bet(bet_id: int, upd_item: BetUpdate, db: Session = Depends(get_db)):
    db_item = db.query(BetDB).filter(BetDB.id == bet_id).first()

    if not db_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bet not found")
    
    for k,v in upd_item.model_dump().items():
        setattr(db_item, k, v)
    
    db.commit()
    db.refresh(db_item)

    return db_item

# API Caio
@app.get('/users')
async def get_users():
    request = requests.get("http://192.168.88.103:8000/users")
    return request.content

# API Sport Monks - Odds
@app.get('/api_odds')
async def get_odds():
    # {{baseUrl}}/:version/:sport/odds/pre-match
    response = requests.get("https://api.sportmonks.com/v3/football/odds/pre-match?api_token=5kmSGVTWIc73kw3gSY9txBnQS1QoR2UfyZ3OEcuKPGQVE3qpMuO9bZZVQFDb")
    data = response.json()

    ids_fixtures = [fixture_id['fixture_id'] for fixture_id in data['data']]

    return ids_fixtures

# API Sport Monks - Matches
@app.get('/api_matches')
async def get_matches():
    # {{baseUrl}}/:version/:sport/fixtures
    # {{baseUrl}}/:version/:sport/odds/pre-match/fixtures/:fixtureId 
    response = requests.get("https://api.sportmonks.com/v3/football/fixtures?api_token=5kmSGVTWIc73kw3gSY9txBnQS1QoR2UfyZ3OEcuKPGQVE3qpMuO9bZZVQFDb")
    data = response.json()

    ids = await get_odds()


    # Iterando sobre os fixtures para acessar o atributo "name"
    # fixture_names = [fixture['name'] for fixture in data['data']]
    
    # return fixture_names

    for fixture in data['data']:
        if fixture['id'] in ids:
            return fixture['name']

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True)
