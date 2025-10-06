# backend/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from .models import Student
from .db import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])

SECRET_KEY = "super_secret_jwt_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str): return pwd_context.hash(password)
def verify_password(plain, hashed): return pwd_context.verify(plain, hashed)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/register")
async def register_user(email: str, password: str, full_name: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Student).where(Student.email == email))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = Student(email=email, full_name=full_name, password_hash=hash_password(password))
    db.add(user)
    await db.commit()
    return {"message": "User registered successfully"}

@router.post("/login")
async def login_user(email: str, password: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Student).where(Student.email == email))
    user = result.scalars().first()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}
