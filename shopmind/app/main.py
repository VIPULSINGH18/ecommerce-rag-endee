"""
ShopMind RAG – E-Commerce Product Search & Q&A
FastAPI application powered by Endee Vector Database
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
import uvicorn

from app.rag_engine import RAGEngine

app = FastAPI(
    title="ShopMind RAG API",
    description="AI-powered e-commerce product search & Q&A using Endee Vector Database",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

rag = RAGEngine()


# ── Schemas ───────────────────────────────────────────────────────────────────

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5
    category: Optional[str] = None
    max_price: Optional[float] = None


class AskRequest(BaseModel):
    question: str
    top_k: int = 4


class IngestRequest(BaseModel):
    force_reingest: bool = False


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <html><body style="font-family:sans-serif;padding:2rem;max-width:640px">
    <h1>🛍️ ShopMind RAG API</h1>
    <p>AI-powered e-commerce search &amp; Q&amp;A via <b>Endee Vector Database</b>.</p>
    <table border="1" cellpadding="6" cellspacing="0">
      <tr><th>Endpoint</th><th>Method</th><th>Purpose</th></tr>
      <tr><td>/health</td><td>GET</td><td>Health check + Endee status</td></tr>
      <tr><td>/ingest</td><td>POST</td><td>Load product catalog into Endee</td></tr>
      <tr><td>/search</td><td>POST</td><td>Semantic product search</td></tr>
      <tr><td>/ask</td><td>POST</td><td>Natural-language Q&amp;A (RAG)</td></tr>
    </table>
    <p><a href="/docs">📖 Interactive Swagger Docs →</a></p>
    </body></html>
    """


@app.get("/health")
def health():
    """Verify Endee connection and index status."""
    status = rag.health_check()
    return {"status": "ok", "endee": status}


@app.post("/ingest")
def ingest(req: IngestRequest = IngestRequest()):
    """
    Ingest the product catalog into Endee vector index.
    Use force_reingest=true to drop and rebuild the index from scratch.
    """
    result = rag.ingest_products(force=req.force_reingest)
    return result


@app.post("/search")
def search(req: SearchRequest):
    """
    Semantic product search powered by Endee.
    Supports optional category and max_price filters.
    """
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
    results = rag.semantic_search(
        query=req.query,
        top_k=req.top_k,
        category=req.category,
        max_price=req.max_price,
    )
    return {"query": req.query, "results": results}


@app.post("/ask")
def ask(req: AskRequest):
    """
    Ask a natural-language question about products.
    RAG pipeline: Endee retrieves relevant products → LLM generates the answer.
    """
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    return rag.ask(question=req.question, top_k=req.top_k)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
