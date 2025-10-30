from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd
import io

population_router = APIRouter()

@population_router.get("/")
def get_population_insight():
    return {"title": "Population", "desc": "Upload CSV to get population insights."}

@population_router.post("/analyze")
async def analyze_population(file: UploadFile = File(...)):
    """Upload a CSV file and generate population insights"""
    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))

        if "Year" not in df.columns or "Population" not in df.columns:
            raise HTTPException(status_code=400, detail="CSV must contain 'Year' and 'Population' columns")

        latest = df.iloc[-1]
        earliest = df.iloc[0]

        growth = ((latest["Population"] - earliest["Population"]) / earliest["Population"]) * 100

        return {
            "title": "Population Growth",
            "start_year": int(earliest["Year"]),
            "end_year": int(latest["Year"]),
            "population_start": int(earliest["Population"]),
            "population_end": int(latest["Population"]),
            "growth_percent": round(growth, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing population: {str(e)}")
