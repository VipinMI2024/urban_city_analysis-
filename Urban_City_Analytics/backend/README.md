# Urban City Analytics Backend (FastAPI)

A batteries-included backend for your Urban City Analytics project.

## Features
- CSV upload endpoint
- Data summary and KMeans clustering on `LAT`/`LONG`
- Folium HTML map generation
- Perplexity API proxy (`/api/perplexity/ask`) — optional; requires `PPLX_API_KEY`
- CORS enabled for easy React integration
- Pytest basic test

## Quickstart

```bash
python -m venv .venv && . .venv/Scripts/activate  # Windows PowerShell
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Open: http://127.0.0.1:8000/docs

## Environment

Create a `.env` file (copy `.env.example`) if you want Perplexity:

```
PPLX_API_KEY=your_api_key_here
PPLX_BASE_URL=https://api.perplexity.ai
```

## API Outline

- `GET /health` — heartbeat
- `POST /api/ingest/csv` — form-data file: CSV
- `POST /api/analytics/summary` — body: `{ "data": [ { ...row }, ... ] }` or `{ "csv": "col1,col2\n..." }`
- `POST /api/analytics/clusters?k=5` — clusters points by `LAT`,`LONG`
- `POST /api/map/folium` — returns saved HTML map path
- `POST /api/perplexity/ask` — body: `{ "question": "Your question" }`

## Notes
- For clustering and map, your data must include columns `LAT` and `LONG`.
- Map file saved to `data/urban_map.html`.

## Project Structure

```
app/
  routers/ (endpoints)
  services/ (logic)
  schemas.py
  main.py
data/
uploads/
```

Happy building!
