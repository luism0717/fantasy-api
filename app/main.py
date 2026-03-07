from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import engine, get_db
from app import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title = "Fantasy Sports API",
    description = "A fantasy sports app build with FastAPI. Made by Luis Mendez.",
    version = "0.1.0"
)

players_db = {
    1: {"name": "Patrick Mahomes", "position": "QB", "nfl_team": "Kansas City Chiefs"},
    2: {"name": "Justin Jefferson", "position": "WR", "nfl_team": "Minnesota Vikings"},
    3: {"name": "Christian McCaffrey", "position": "RB", "nfl_team": "San Francisco 49ers"}
}

#That request → route → function → response
@app.get("/")
def root():
    return {"message": "Fantasy API is alive!"}

@app.get("/players")
def getPlayers(db: Session = Depends(get_db)):
    players = db.query(models.Player).all()
    return players

@app.get("/players/{player_id}")
def getPlayer(player_id: int, db: Session = Depends(get_db)):
    player = db.query(models.Player).filter(models.Player.id == player_id).first()
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return player

class Player(BaseModel):
    name: str
    position: str
    nfl_team: str

@app.post("/players")
def createPlayer(player: Player, db: Session = Depends(get_db)):
    db_player = models.Player(
        name=player.name,
        position=player.position,
        nfl_team=player.nfl_team
    )
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player

@app.delete("/players/{player_id}")
def removePlayer(player_id: int, db: Session = Depends(get_db)):
    player =  db.query(models.Player).filter(models.Player.id == player_id).first()
    if player is None:
        raise HTTPException(status_code=404, detail="Player ID not found")
    db.delete(player)
    db.commit()
    return player