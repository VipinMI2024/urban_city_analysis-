from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.ml import ml_router # import the ML router
import os, pandas as pd, io, folium
from fastapi import UploadFile, File, HTTPException

# ---------------------------
# FastAPI app
# ---------------------------
app = FastAPI(title="Urban City Analytics Full Backend")

# ---------------------------
# Enable CORS
# ---------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# Static Files (maps)
# ---------------------------
MAPS_DIR = "static/maps"
os.makedirs(MAPS_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# ---------------------------
# Include ML Router
# ---------------------------
app.include_router(ml_router, prefix="/ml", tags=["ML"])

# ---------------------------
# Keep your other endpoints as before
# ---------------------------
@app.get("/population")
def get_population():
    return [
        {"year": 2020, "population": 1000000},
        {"year": 2021, "population": 1050000},
        {"year": 2022, "population": 1100000}
    ]

@app.get("/air_quality")
def get_air_quality():
    return {"title": "Air Quality", "desc": "Current AQI: 78 (Moderate). Main pollutant: PM2.5."}

@app.get("/traffic")
def get_traffic():
    return {"title": "Traffic", "desc": "Peak congestion between 8–10 AM and 6–8 PM."}

@app.get("/infrastructure")
def get_infrastructure():
    return {"title": "Infrastructure", "desc": "10 new metro stations under development."}

@app.get("/economy")
def get_economy():
    return {"title": "Economy", "desc": "IT sector hiring increased by 18% this year."}

@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        return {"columns": list(df.columns), "rows": len(df)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid CSV file: {str(e)}")

@app.post("/analytics/summary")
async def analytics_summary(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        summary = df.describe(include="all").fillna("NaN").to_dict()
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing file: {str(e)}")

@app.post("/map/folium")
async def folium_map(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))

        if "LAT" not in df.columns or "LONG" not in df.columns:
            raise HTTPException(status_code=400, detail="CSV must contain LAT and LONG columns")

        m = folium.Map(location=[df["LAT"].mean(), df["LONG"].mean()], zoom_start=12)
        for _, row in df.iterrows():
            folium.CircleMarker(
                location=[row["LAT"], row["LONG"]],
                radius=5,
                popup=str(row.to_dict()),
                color="blue",
                fill=True,
                fill_color="blue"
            ).add_to(m)

        map_path = os.path.join(MAPS_DIR, "urban_map.html")
        m.save(map_path)
        return {"map_url": "/static/maps/urban_map.html"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating map: {str(e)}")
