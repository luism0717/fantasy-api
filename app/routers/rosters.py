from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.security import get_current_user

router = APIRouter(prefix="/rosters", tags=["Rosters"])

@router.post("/")
def add_to_roster(roster: schemas.RosterAdd, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    existing = db.query(models.Roster).filter(
        models.Roster.player_id == roster.player_id,
        models.Roster.team_id == roster.team_id
    ).first()

    if existing is not None:
        raise HTTPException(status_code=400, detail="Player already on this roster")
    
    db_roster = models.Roster(
        team_id = roster.team_id,
        player_id = roster.player_id
    )
    db.add(db_roster)
    db.commit()
    db.refresh(db_roster)

    return db_roster

@router.get("/{team_id}")
def get_team_roster(team_id: int, db: Session = Depends(get_db)):
    return db.query(models.Roster).filter(models.Roster.team_id == team_id).all()

@router.delete("/{roster_id}")
def remove_from_roster(roster_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    roster = db.query(models.Roster).filter(models.Roster.id == roster_id).first()
    if roster is None:
        raise HTTPException(status_code=404, detail="Roster entry not found")
    
    db.delete(roster)
    db.commit()

    return roster