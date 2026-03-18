from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.security import get_current_user
import random
import string

router = APIRouter(prefix="/leagues", tags=["Leagues"])

@router.post("/", status_code=201)
def create_league(league: schemas.CreateLeague, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_league = models.League(
        name=league.name,
        sport=league.sport,
        max_teams=league.max_teams,
        invite_code="".join(random.choices(string.ascii_uppercase + string.digits, k=6)),
        commissioner_id=current_user.id
    )
    db.add(db_league)
    db.commit()
    db.refresh(db_league)

    return db_league

@router.get("/")
def get_leagues(db: Session = Depends(get_db)):
    return db.query(models.League).all()

@router.get("/{league_id}")
def get_league(league_id: int, db: Session = Depends(get_db)):
    league = db.query(models.League).filter(models.League.id == league_id).first()
    if league is None:
        raise HTTPException(status_code=404, detail="League ID not found")
    
    return league

@router.post("/{league_id}/join", status_code=201)
def join_league(team: schemas.CreateTeam, league_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    league = db.query(models.League).filter(models.League.id == league_id).first()
    if league is None:
        raise HTTPException(status_code=404, detail="League not found")
    
    leagueInvite = db.query(models.League).filter(models.League.invite_code == team.invite_code).first()
    if leagueInvite is None:
        raise HTTPException(status_code=403, detail="Invalid invite code")
    
    leagueCapacity = db.query(models.Team).filter(models.Team.league_id == league_id).count()
    if leagueCapacity >= league.max_teams:
        raise HTTPException(status_code=400, detail="League is full")
    
    db_team = models.Team(
        name = team.name,
        total_points = 0,
        league_id = league_id,
        owner_id = current_user.id
    )
    db.add(db_team)
    db.commit()
    db.refresh(db_team)

    return db_team