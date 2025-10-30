from fastapi import APIRouter, UploadFile, File
import pandas as pd
import os

router = APIRouter()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    # Save file locally
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Load CSV/Excel into pandas for analytics
    try:
        if file.filename.endswith(".csv"):
            df = pd.read_csv(file_path)
        elif file.filename.endswith((".xls", ".xlsx")):
            df = pd.read_excel(file_path)
        else:
            return {"error": "Only CSV or Excel files are supported"}

        # Example: return first 5 rows for preview
        return {"message": "File uploaded successfully", "preview": df.head().to_dict(orient="records")}
    except Exception as e:
        return {"error": str(e)}
