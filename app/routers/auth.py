from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.database import get_db
from app import models, schemas
from app.security import hash_password, verify_password, create_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register_user(user_register: schemas.UserRegister, db: Session = Depends(get_db)):
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

@router.post("/login")
def login_user(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()

    if user  is None:
        raise HTTPException(status_code=401, detail="User not found")
    
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Wrong Password")
    
    token = create_token({"sub": str(user.id)})

    return {"access_token": token, "token_type": "bearer"}