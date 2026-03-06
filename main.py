from fastapi import FastAPI

app = FastAPI(
    title = "Fantasy Sports API",
    description = "A fantasy sports app build with FastAPI. Made by Luis Mendez.",
    version = "0.1.0"
)

#That request → route → function → response
@app.get("/")
def root():
    return {"message": "Fantasy API is alive!"}

@app.get("/players")
def playerInfo():
    return [
        {"name": "Patrick Mahomes", "position": "QB", "nfl_team": "Kansas City Chiefs"},
        {"name": "Justin Jefferson", "position": "WR", "nfl_team": "Minnesota Vikings"},
        {"name": "Christian McCaffrey", "position": "RB", "nfl_team": "San Francisco 49ers"}
    ]