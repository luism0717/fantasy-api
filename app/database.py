from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# This is the connection string - it tells SQLAlchemy where your database is
DATABASE_URL = "postgresql://fantasy_user:password123@localhost/fantasy_db"

# The engine is the actual connection to the database
engine = create_engine(DATABASE_URL)

# Each request to your API gets its own database session
SessionLocal = sessionmaker(autocommit=False, autoFlush=False, bind=engine)

# All your database models will inerit from this
Base = declarative_base()

# This function gives routes a database sesion and closes it when done
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()