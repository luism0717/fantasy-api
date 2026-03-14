from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app import models
from app.database import engine, get_db
from app.security import hash_password, verify_password, create_token, get_current_user
import random
import string

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

# Pydantic models 
class Player(BaseModel):
    name: str
    position: str
    nfl_team: str

@app.post("/players")
def createPlayer(player: Player, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
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

# Pydantic models 
class UserRegister(BaseModel):
    username: str
    email: str
    password: str

@app.post("/auth/register")
def registerUser(user_register: UserRegister, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_register.email).first()
    if user is not None:
        raise HTTPException(status_code=400, detail="Email already exists.")
    db_user = models.User(
        username=user_register.username,
        email=user_register.email,
        hashed_password=hash_password(user_register.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/auth/login")
def loginUser(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if user  is None:
        raise HTTPException(status_code=401, detail="User not found")
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Wrong Password")
    token = create_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

class CreateLeague(BaseModel):
    name: str
    sport: str = "nfl"
    max_teams: int = 10

@app.post("/leagues")
def createLeague(league: CreateLeague, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
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

@app.get("/leagues")
def getLeagues(db: Session = Depends(get_db)):
    leagues = db.query(models.League).all()
    return leagues

@app.get("/leagues/{league_id}")
def getLeague(league_id: int, db: Session = Depends(get_db)):
    league = db.query(models.League).filter(models.League.id == league_id).first()
    if league is None:
        raise HTTPException(status_code=404, detail="League ID not found")
    return league

class CreateTeam(BaseModel):
    name: str
    invite_code: str

@app.post("/leagues/{league_id}/join")
def joinLeague(team: CreateTeam, league_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
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

class RosterAdd(BaseModel):
    team_id: int
    player_id: int

@app.post("/rosters")
def addToRoster(roster: RosterAdd, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
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

@app.get("/rosters/{team_id}")
def getTeamsRoster(team_id: int, db: Session = Depends(get_db)):
    team = db.query(models.Roster).filter(models.Roster.team_id == team_id).all()
    return team

@app.delete("/rosters/{roster_id}")
def removePlayerFromRoster(roster_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    roster = db.query(models.Roster).filter(models.Roster.id == roster_id).first()
    if roster is None:
        raise HTTPException(status_code=404, detail="Roster entry not found")
    db.delete(roster)
    db.commit()
    return roster