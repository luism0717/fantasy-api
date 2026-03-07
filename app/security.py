from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

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
    expire = datetime.utcnow() + timedelta(minutes=EXPIRE_MINUTES)
    payload.update({"exp": expire})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)