import io
import pandas as pd
from typing import Dict, Any
from sklearn.cluster import KMeans

REQUIRED_LAT = "LAT"
REQUIRED_LONG = "LONG"

def read_csv_bytes(data: bytes, **kwargs) -> pd.DataFrame:
    return pd.read_csv(io.BytesIO(data), **kwargs)

def summarize_df(df: pd.DataFrame) -> Dict[str, Any]:
    return {
        "n_rows": int(df.shape[0]),
        "n_cols": int(df.shape[1]),
        "columns": [str(c) for c in df.columns.tolist()],
        "dtypes": {str(c): str(t) for c, t in df.dtypes.items()},
        "null_counts": {str(c): int(df[c].isna().sum()) for c in df.columns},
    }

def kmeans_clusters(df: pd.DataFrame, k: int = 5) -> pd.DataFrame:
    if REQUIRED_LAT not in df.columns or REQUIRED_LONG not in df.columns:
        raise ValueError(f"DataFrame must contain '{REQUIRED_LAT}' and '{REQUIRED_LONG}' columns.")
    coords = df[[REQUIRED_LAT, REQUIRED_LONG]].dropna()
    if coords.empty:
        raise ValueError("No valid coordinate rows to cluster.")
    # KMeans requires k <= number of samples
    k = max(1, min(k, len(coords)))
    km = KMeans(n_clusters=k, n_init="auto", random_state=42)
    labels = km.fit_predict(coords)
    out = coords.copy()
    out["cluster"] = labels
    return out
