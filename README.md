# FANTASY Sports API

A production-ready REST API for a fantasy sports app built from scratch with **FastAPI** and **PostgreSQL**. Built as a learning project to learn new techstacks.

---

## Live Demo

**Interactive API Docs:** https://web-production-eb184.up.railway.app/docs

No setup needed - open the link, click any endpoint, and test it live.

---

## Tech Stack

| Layer | Tool | Why I chose it |
|---|---|---|
| Framework | FastAPI | Modern Python framework with automatic docs generation |
| Database | PostgreSQL | Industry-standard relational database |
| ORM | SQLAlchemy | Type-safe database queries without writing raw SQL |
| Auth | JWT (python-jose) | Stateless authentication - learned how tokens work under the hood |
| Password Hashing | bcrypt (passlib) | Industry standard - never store plain text passwords |
| Testing | pytest + httpx | Isolated test suite with a separate test database |
| Hosting | Railway | Simple cloud deployment connected to GitHub |

---

## Project Structure
```
app/
├── main.py          # App entry point — registers all routers
├── models.py        # SQLAlchemy database table definitions
├── schemas.py       # Pydantic request/response models
├── database.py      # PostgreSQL connection and session management
├── security.py      # JWT token creation and validation
└── routers/
    ├── auth.py      # Register and login endpoints
    ├── players.py   # Player CRUD endpoints
    ├── leagues.py   # League management endpoints
    └── rosters.py   # Roster management endpoints
tests/
├── conftest.py      # Shared test config and isolated test database
├── test_auth.py     # Auth endpoint tests
├── test_players.py  # Player endpoint tests
├── test_leagues.py  # League endpoint tests
└── test_rosters.py  # Roster endpoint tests
```

---

## API Endpoints

| Method | Route | Auth | Description |
|---|---|---|---|
| GET | `/players` | No | List all players |
| GET | `/players/{id}` | No | Get one player |
| POST | `/players` | Yes | Add a player |
| DELETE | `/players/{id}` | Yes | Remove a player |
| POST | `/auth/register` | No | Create account |
| POST | `/auth/login` | No | Get JWT token |
| GET | `/leagues` | No | List all leagues |
| GET | `/leagues/{id}` | No | Get one league |
| POST | `/leagues` | Yes | Create a league |
| POST | `/leagues/{id}/join` | Yes | Join with invite code |
| POST | `/rosters` | Yes | Add player to roster |
| GET | `/rosters/{team_id}` | No | Get team roster |
| DELETE | `/rosters/{id}` | Yes | Drop a player |

---

## Run Locally

**1. Clone and install dependencies**
```bash
git clone https://github.com/luism0717/fantasy-api
cd fantasy-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**2. Set up PostgreSQL**
```bash
sudo -i -u postgres
psql
CREATE DATABASE fantasy_db;
CREATE USER fantasy_user WITH PASSWORD 'password123';
GRANT ALL PRIVILEGES ON DATABASE fantasy_db TO fantasy_user;
\c fantasy_db
GRANT ALL ON SCHEMA public TO fantasy_user;
\q
exit
```

**3. Create a `.env` file**
```
DATABASE_URL=postgresql://fantasy_user:password123@localhost/fantasy_db
SECRET_KEY=your-secret-key
```

**4. Run the server**
```bash
uvicorn app.main:app --reload
```

**5. Open the docs**
Visit `http://localhost:8000/docs`

---

## Run Tests
```bash
pytest tests/ -v
```

Tests run against an isolated `fantasy_test_db` database — your real data is never touched. 17 tests covering auth, players, leagues, and rosters.

---

## Future Features

- [ ] Live scoring by syncing with a sports data API
- [ ] Weekly matchup system
- [ ] Player stats and fantasy point calculation
- [ ] React frontend
- [ ] Waiver wire system for adding/dropping players

---

## What I Learned

- Design and build a REST API from scratch
- How JWT authentication works under the hood
- Writing SQL relationships with SQLAlchemy ORM
- Writing a test suite with an isolated test database
- Deploying a Python app to production with Railway