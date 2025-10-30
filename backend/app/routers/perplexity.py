from fastapi import APIRouter
from ..schemas import PerplexityQuestion
from ..services.perplexity_client import ask_perplexity

router = APIRouter(prefix="/perplexity", tags=["perplexity"])

@router.post("/ask")
def ask(q: PerplexityQuestion):
    result = ask_perplexity(q.question)
    return result
