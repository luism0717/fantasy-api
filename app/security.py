from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db

# Tells passlib to use bcrypto for hashing
pwd_context = CryptContext (schemes=["bcrypt"], deprecated="auto")

# Change this to a long random string in production - this signs your tokens
SECRET_KEY = "changethiskey"
ALGORITHM = "HS256"
EXPIRE_MINUTES = 60 * 24 # 1 day

def hash_password(password: str) -> str:
    """Turn a plain password into a secure hash."""
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    """Check if a plain password matches the stored hash."""
    return pwd_context.verify(plain, hashed)

def create_token(data: dict) -> str:
    """Create a signed JWT token that expired after EXPIRE_MINUTES."""
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_MINUTES)
    payload.update({"exp": expire})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    from app import models
    user = db.query(models.User).filter(models.User.id == int(user_id)).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user
