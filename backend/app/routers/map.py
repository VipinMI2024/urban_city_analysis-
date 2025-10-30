from fastapi import APIRouter, HTTPException
import os
import pandas as pd
from ..schemas import FoliumMapResponse
from ..services.map_service import build_map, save_map

router = APIRouter(prefix="/map", tags=["map"])

DATA_FILE = os.path.join("data", "map.csv")  # 👈 Path to map.csv

@router.get("/folium", response_model=FoliumMapResponse)
def folium_map():
    """Generate Folium map from saved map.csv"""
    if not os.path.exists(DATA_FILE):
        raise HTTPException(status_code=404, detail="map.csv file not found in data/ folder")

    try:
        df = pd.read_csv(DATA_FILE)

        if df.empty:
            raise HTTPException(status_code=400, detail="map.csv is empty")

        # Build and save map
        m = build_map(df)
        map_path = os.path.join("data", "urban_map.html")
        save_map(m, map_path)

        return FoliumMapResponse(map_file=map_path)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating map: {str(e)}")
