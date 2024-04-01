from fastapi import FastAPI, HTTPException, Response, status, Depends
from sqlalchemy.orm import Session
from database import *
from models import *
from typing import List
import requests

app = FastAPI()

tokens = []

# API Caio - Users
@app.get('/users')
async def get_users():
    request = requests.get("http://192.168.88.103:8000/users")
    return request.content

# API Caio - Matches
@app.get('/get/matches')
async def get_matches(id: int):
    request = requests.get(f"http://192.168.88.103:8000/api/matches/{id}")
    return request.content

# API Sport Monks - Odds
@app.get('/api/match/{id}')
async def get_od_by_id(id: int):
    
    response = requests.get(f'https://api.sportmonks.com/v3/football/odds/pre-match/fixtures/{id}?api_token=5kmSGVTWIc73kw3gSY9txBnQS1QoR2UfyZ3OEcuKPGQVE3qpMuO9bZZVQFDb')
    
    data = response.json()
    lista = []
    
    for match in data['data']:
        objetoWinner = {}
        
        if match['market_description'] == 'Match Winner':
            
            if match['label'] == 'Away':
                
                yorno = False
                for i in lista:
                    if i['label'] == 'Away':
                        yorno = True
                        break
                        
                if not yorno: 
                    objetoWinner['label'] = match['label']
                    objetoWinner['odd'] = match['value']
                    lista.append(objetoWinner)
                
            elif match['label'] == 'Home':
                
                yorno = False 
                for i in lista:
                    if i['label'] == 'Home':
                        yorno = True
                        break
                        
                if not yorno:  
                    objetoWinner['label'] = match['label']
                    objetoWinner['odd'] = match['value']
                    lista.append(objetoWinner)
                                      
    return lista

# 'response_model' serve para dizer qual tipo de retorno a função vai ter, nesse caso vai ser o tipo ItemRead, um modelo criado no arquivo models.py
@app.post('/create_bet', response_model=BetRead)
async def create_bet(id: int, item: BetCreate, db: Session = Depends(get_db)):
    exists = db.query(BetDB).filter(BetDB.name == item.name).first()

    if exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="name is already created")
    
    odds = await get_od_by_id(id)
    matches = await get_matches(id)

    name = matches['name']

    print(odds)

    for odd in odds:
        if item.team == 'Away' and odd['label'] == 'Away':
            value_odd = odd['odd']
            break
        elif item.team == 'Home' and odd['label'] == 'Home':
            value_odd = odd['odd']
            break

    # Converte o pydantic para um dicionario
    db_item = BetDB(name=name, odd=value_odd, price=item.price, team=item.team)
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

@app.delete('/delete_bet/{bet_id}')
async def delete_bet(bet_id: int, db: Session = Depends(get_db)):
    db_item = db.query(BetDB).filter(BetDB.id == bet_id).first()

    if db_item:
        db.delete(db_item)
        db.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bet not found")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host='0.0.0.0', port=8001, reload=True)
