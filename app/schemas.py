from pydantic import BaseModel

# Pydantic models 
class Player(BaseModel):
    name: str
    position: str
    nfl_team: str

class UserRegister(BaseModel):
    username: str
    email: str
    password: str

class CreateLeague(BaseModel):
    name: str
    sport: str = "nfl"
    max_teams: int = 10

class CreateTeam(BaseModel):
    name: str
    invite_code: str

class RosterAdd(BaseModel):
    team_id: int
    player_id: int