from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
import pandas as pd
import os
from ..deps import ensure_dirs
from ..schemas import UploadResponse
from ..services.analytics import read_csv_bytes

router = APIRouter(prefix="/ingest", tags=["ingest"])

@router.post("/csv", response_model=UploadResponse)
async def upload_csv(file: UploadFile = File(...), settings=Depends(ensure_dirs)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only .csv files are supported.")
    raw = await file.read()
    try:
        df = read_csv_bytes(raw)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse CSV: {e}")
    save_path = os.path.join(settings.UPLOAD_DIR, file.filename)
    df.to_csv(save_path, index=False)
    return UploadResponse(filename=save_path, rows=int(df.shape[0]), columns=[str(c) for c in df.columns])
