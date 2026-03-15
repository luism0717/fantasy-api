from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.security import get_current_user

router = APIRouter(prefix="/players", tags=["Players"])

@router.get("/")
def get_players(db: Session = Depends(get_db)):
    players = db.query(models.Player).all()
    
    return players

@router.get("/{player_id}")
def get_player(player_id: int, db: Session = Depends(get_db)):
    player = db.query(models.Player).filter(models.Player.id == player_id).first()
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    
    return player

@router.post("/", status_code=201)
def create_player(player: schemas.Player, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_player = models.Player(
        name=player.name,
        position=player.position,
        nfl_team=player.nfl_team
    )
    db.add(db_player)
    db.commit()
    db.refresh(db_player)

    return db_player

@router.delete("/{player_id}")
def remove_player(player_id: int, db: Session = Depends(get_db)):
    player =  db.query(models.Player).filter(models.Player.id == player_id).first()
    if player is None:
        raise HTTPException(status_code=404, detail="Player ID not found")
    
    db.delete(player)
    db.commit()

    return player