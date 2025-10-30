from typing import Optional
import folium
import pandas as pd
from branca.colormap import linear

def build_map(df: pd.DataFrame, lat_col: str = "LAT", long_col: str = "LONG", stage_col: Optional[str] = "STAGE") -> folium.Map:
    if df.empty:
        # default world view
        m = folium.Map(location=[0,0], zoom_start=2)
        return m
    m = folium.Map(location=[df[lat_col].mean(), df[long_col].mean()], zoom_start=11)
    palette = linear.Set1_09.scale(0, 8)
    for _, row in df.dropna(subset=[lat_col, long_col]).iterrows():
        stage = str(row.get(stage_col, "")) if stage_col in df.columns else ""
        idx = hash(stage) % 9 if stage else 0
        color = palette(idx)
        folium.CircleMarker(
            location=[float(row[lat_col]), float(row[long_col])],
            radius=5, tooltip=f"Stage: {stage}" if stage else None,
            color=color, fill=True, fill_opacity=0.7
        ).add_to(m)
    return m

def save_map(m: folium.Map, path: str) -> str:
    m.save(path)
    return path
