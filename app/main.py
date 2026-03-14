from fastapi import FastAPI
from app.database import engine
from app import models
from app.routers import players, auth, leagues, rosters

models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title = "Fantasy Sports API",
    description = "A fantasy sports app build with FastAPI. Made by Luis Mendez.",
    version = "0.1.0"
)

#That request → route → function → response
app.include_router(players.router)
app.include_router(auth.router)
app.include_router(leagues.router)
app.include_router(rosters.router)

@app.get("/", tags=["Health"])
def root():
    return {"message": "Fantasy API is alive!"}