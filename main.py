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