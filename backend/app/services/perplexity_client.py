from typing import Any, Dict
import requests
from ..config import get_settings

def ask_perplexity(question: str) -> Dict[str, Any]:
    settings = get_settings()
    if not settings.PPLX_API_KEY:
        return {
            "ok": False,
            "error": "PPLX_API_KEY not set. Add it to your environment or .env file.",
        }
    url = settings.PPLX_BASE_URL.rstrip('/') + "/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.PPLX_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "sonar-small-online",  # common default; change as desired
        "messages": [{"role": "user", "content": question}],
        "temperature": 0.2,
        "stream": False,
    }
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        return {"ok": True, "data": data}
    except Exception as e:
        return {"ok": False, "error": str(e)}
