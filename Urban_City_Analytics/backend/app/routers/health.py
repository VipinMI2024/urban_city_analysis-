from fastapi import APIRouter
from ..schemas import Health

router = APIRouter(tags=["health"])

@router.get("/health", response_model=Health)
def health():
    return Health(status="ok", app="Urban City Analytics Backend", version="1.0.0")
