from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class Health(BaseModel):
    status: str = "ok"
    app: str
    version: str

class UploadResponse(BaseModel):
    filename: str
    rows: int
    columns: List[str]

class SummaryStats(BaseModel):
    n_rows: int
    n_cols: int
    columns: List[str]
    dtypes: Dict[str, str]
    null_counts: Dict[str, int]

class ClusterPoint(BaseModel):
    lat: float = Field(..., alias="LAT")
    long: float = Field(..., alias="LONG")
    cluster: int

class ClusterResponse(BaseModel):
    n_clusters: int
    points: List[ClusterPoint]

class FoliumMapResponse(BaseModel):
    map_file: str

class PerplexityQuestion(BaseModel):
    question: str
