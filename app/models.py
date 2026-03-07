from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.sql import func
from app.database import Base

class Player(Base):
    __tablename__ = "players"

    id  =      Column(Integer, primary_key=True, index=True)
    name =     Column(String, nullable=False)
    position = Column(String, nullable=False)
    nfl_team = Column(String, nullable=False)
    
class User(Base):
    __tablename__ = "users"

    id =              Column(Integer, primary_key=True, index=True)
    username =        Column(String, nullable=False, unique=True)
    email =           Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    created_at =      Column(DateTime(timezone=True), server_default=func.now())

class League(Base):
    __tablename__ = "leagues"

    id =              Column(Integer, primary_key=True, index=True)
    name =            Column(String, nullable=False)
    invite_code =     Column(String, nullable=False, unique=True)
    sport =           Column(String, default="nfl")
    max_teams =       Column(Integer, default=10)
    commissioner_id = Column(Integer, ForeignKey("users.id"))

class Team(Base):
    __tablename__ = "teams"

    id =           Column(Integer, primary_key=True, index=True)
    name =         Column(String, nullable=False)
    total_points = Column(Float, default=0.0)
    league_id =    Column(Integer, ForeignKey("leagues.id"))
    owner_id =     Column(Integer, ForeignKey("users.id"))

class Roster(Base):
    __tablename__ = "rosters"

    id =          Column(Integer, primary_key=True, index=True)
    team_id =     Column(Integer, ForeignKey("teams.id"))
    player_id =   Column(Integer, ForeignKey("players.id"))
    is_starter =  Column(Boolean, default=True)
    acquired_at = Column(DateTime(timezone=True), server_default=func.now())

