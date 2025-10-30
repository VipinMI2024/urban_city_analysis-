import os
from fastapi import Depends
from .config import get_settings, Settings

def ensure_dirs(settings: Settings = Depends(get_settings)) -> Settings:
    os.makedirs(settings.DATA_DIR, exist_ok=True)
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    return settings
