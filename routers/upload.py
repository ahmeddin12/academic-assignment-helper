# backend/routers/upload.py
from fastapi import APIRouter, UploadFile, File, Depends
import os, shutil, uuid
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import Assignment
from ..db import get_db

router = APIRouter(prefix="/upload", tags=["Upload"])

UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/")
async def upload_assignment(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    filename = f"{uuid.uuid4().hex}_{file.filename}"
    path = os.path.join(UPLOAD_DIR, filename)

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_assignment = Assignment(filename=file.filename, filepath=path)
    db.add(new_assignment)
    await db.commit()
    return {"message": "File uploaded successfully", "file_path": path}
