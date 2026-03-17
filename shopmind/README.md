# 🛍️ ShopMind RAG — AI-Powered E-Commerce Product Search

> **Retrieval-Augmented Generation (RAG) for e-commerce** — find products semantically and get intelligent answers to shopping questions, powered by **[Endee Vector Database](https://github.com/endee-io/endee)** and FastAPI.

---

## 📌 Problem Statement

Traditional keyword-based e-commerce search fails when customers describe what they want in natural language. Searching for *"something warm for winter camping"* or *"a gift for a coffee lover"* returns no results because no product is literally named that way.

**ShopMind** solves this with a full RAG pipeline:

1. **Embed** every product description using a sentence-transformer model.
2. **Store** those embeddings in **Endee** — a high-performance open-source vector database.
3. **Retrieve** the most semantically relevant products for any natural-language query.
4. **Generate** a human-friendly answer with an LLM grounded in the retrieved products.

---

## 🏗️ System Design

```
┌─────────────────────────────────────────────────────────────────────┐
│                         ShopMind Architecture                        │
│                                                                       │
│  User Query                                                           │
│      │                                                                │
│      ▼                                                                │
│  ┌─────────────┐    embed     ┌──────────────────┐                   │
│  │  FastAPI    │─────────────►│ SentenceTransfor │                   │
│  │  (main.py)  │              │ mer (MiniLM-L6)  │                   │
│  └──────┬──────┘              └────────┬─────────┘                   │
│         │                              │ 384-dim vector               │
│         │                              ▼                              │
│         │                    ┌─────────────────────┐                 │
│         │    top-k results   │   Endee Vector DB   │                 │
│         │◄───────────────────│  (HNSW + cosine)    │                 │
│         │                    │  + filter: category │                 │
│         │                    │             price   │                 │
│         │                    └─────────────────────┘                 │
│         │                                                             │
│         │  (for /ask only)                                            │
│         ▼                                                             │
│  ┌─────────────┐  augmented   ┌──────────────────┐                   │
│  │  RAG Engine │─────prompt──►│  GPT-4o-mini     │                   │
│  │ (rag_engine)│              │  (or fallback)   │                   │
│  └─────────────┘              └────────┬─────────┘                   │
│                                        │ natural-language answer      │
│                                        ▼                              │
│                               Response to User                        │
└─────────────────────────────────────────────────────────────────────┘
```

### Key components

| Component | Technology | Role |
|---|---|---|
| **API server** | FastAPI + Uvicorn | REST endpoints for search & Q&A |
| **Vector DB** | **Endee** (self-hosted via Docker) | Stores/queries product embeddings |
| **Embeddings** | `all-MiniLM-L6-v2` (384 dim) | Converts text → dense vectors |
| **LLM** | GPT-4o-mini (OpenAI) | Generates grounded answers |
| **Filters** | Endee `$eq` / `$range` | Category + price-range filtering |

---

## 🔍 How Endee Is Used

Endee is the **central retrieval engine** of ShopMind. Every interaction with the product catalog goes through it:

### 1 — Index Creation
```python
client.create_index(
    name="ecom_products",
    dimension=384,       # matches MiniLM-L6-v2 output
    space_type="cosine", # cosine similarity for text embeddings
    precision=Precision.INT8,  # memory-efficient quantisation
)
```

### 2 — Upsert (Ingestion)
Each product is embedded and stored with **metadata** (for display) and **filters** (for narrowing results):
```python
index.upsert([{
    "id":     "elec-001",
    "vector": embed("ProSound X3 Wireless Headphones. Premium over-ear..."),
    "meta":   {"name": "...", "price": 249, "brand": "...", ...},
    "filter": {"category": "electronics", "price_int": 249},
}])
```

### 3 — Semantic Search
```python
results = index.query(
    vector=embed(user_query),
    top_k=5,
    filter=[
        {"category": {"$eq": "sports"}},
        {"price_int": {"$range": [0, 100]}},
    ],
    filter_boost_percentage=20,  # compensate for filter-narrowed HNSW search
)
```

### 4 — RAG Context Assembly
The retrieved product metadata is formatted into a prompt context that grounds the LLM answer — preventing hallucination and ensuring responses reflect real inventory.

---

## 📂 Project Structure

```
ecommerce-rag-endee/          ← forked Endee repo
├── shopmind/                 ← ShopMind project lives here
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── rag_engine.py
│   │   └── catalog.py
│   ├── scripts/
│   │   └── demo.py
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── requirements.txt
│   ├── .env.example
│   ├── .gitignore
│   ├── LICENSE
│   └── README.md
├── src/                      ← Endee's original source
├── infra/                    ← Endee's original files
└── ...
```

---

## 🚀 Setup & Execution

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) & Docker Compose v2
- Python 3.10+ (for local dev only)
- OpenAI API key *(optional — enables natural-language answers)*

---

### Option A — Docker Compose (Recommended ✅)

**1. Clone this repo**
```bash
git clone https://github.com/VIPULSINGH18/ecommerce-rag-endee.git
cd ecommerce-rag-endee/shopmind
```

**2. Configure environment**
```bash
cp .env.example .env
# Edit .env — add your OPENAI_API_KEY if you have one
```

**3. Start everything**
```bash
docker compose up -d
```

This starts:
- `endee-server` on `http://localhost:8080`
- `shopmind-api` on `http://localhost:8000`

**4. Load the product catalog**
```bash
curl -X POST http://localhost:8000/ingest \
     -H "Content-Type: application/json" \
     -d '{"force_reingest": false}'
```

**5. Try it out**
```bash
# Semantic search
curl -X POST http://localhost:8000/search \
     -H "Content-Type: application/json" \
     -d '{"query": "noise cancelling headphones for travel", "top_k": 3}'

# RAG Q&A
curl -X POST http://localhost:8000/ask \
     -H "Content-Type: application/json" \
     -d '{"question": "What is a good gift for a coffee lover under $200?"}'

# Filtered search – sports gear under $100
curl -X POST http://localhost:8000/search \
     -H "Content-Type: application/json" \
     -d '{"query": "home gym equipment", "category": "sports", "max_price": 100}'
```

---

### Option B — Local Development

**1. Start Endee via Docker**
```bash
docker run -d \
  --name endee-server \
  -p 8080:8080 \
  -v endee-data:/data \
  endeeio/endee-server:latest
```

**2. Create and activate virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure**
```bash
cp .env.example .env
# Edit .env
```

**5. Run the API**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**6. Open Swagger UI** → [http://localhost:8000/docs](http://localhost:8000/docs)

---

### Option C — Run the Demo Script

After the API is running and the catalog is ingested:
```bash
python scripts/demo.py
```

Expected output:
```
============================================================
  1. Health Check
============================================================
{"status": "ok", "endee": {"connected": true, "catalog_loaded": true, ...}}

============================================================
  3. Semantic Search – 'noise cancelling headphones for travel'
============================================================
  [0.891] ProSound X3 Wireless Noise-Cancelling Headphones – $249
  [0.762] EchoSmart 4 Smart Speaker – $129
  [0.701] VisionTab Pro 11 Tablet – $499
...
```

---

## 🌐 API Reference

### `GET /health`
Returns Endee connection status and loaded indexes.

### `POST /ingest`
Load the product catalog into Endee.

```json
{ "force_reingest": false }
```

### `POST /search`
Semantic product search with optional filters.

```json
{
  "query": "wireless headphones for gym",
  "top_k": 5,
  "category": "electronics",
  "max_price": 200
}
```

**Available categories:** `electronics` · `clothing` · `home` · `sports` · `beauty`

### `POST /ask`
Natural-language Q&A powered by RAG.

```json
{ "question": "What's good for someone who travels a lot?", "top_k": 4 }
```

Response:
```json
{
  "question": "What's good for someone who travels a lot?",
  "answer": "For frequent travellers I recommend the ProSound X3 headphones for in-flight comfort...",
  "sources": [{"id": "elec-001", "name": "ProSound X3 Wireless Headphones"}, ...]
}
```

---

## 🧪 Example Queries to Try

| Query | Type | Notes |
|---|---|---|
| `"noise cancelling headphones"` | Semantic search | Pure vector similarity |
| `"warm clothes for winter"` | Semantic search | Cross-category intent |
| `"home gym under $100"` | Filtered search | Price + vector |
| `"gift for a coffee lover"` | RAG Q&A | Intent understanding |
| `"best skincare routine for travel"` | RAG Q&A | Multi-product answer |
| `"waterproof outdoor gear"` | Filtered search | Category = clothing |

---

## 👨‍💻 Author
**Vipul Singh**
- GitHub: [@VIPULSINGH18](https://github.com/VIPULSINGH18)
- Email: vipulsingh7235@gmail.com
- LinkedIn: https://www.linkedin.com/in/vipulsk04/

## 📄 License

This project is licensed under the Apache-2.0 License — 
the same license as the Endee Vector Database it builds upon.

---

## 🙏 Acknowledgements

- [Endee](https://endee.io) — high-performance open-source vector database
- [sentence-transformers](https://www.sbert.net/) — `all-MiniLM-L6-v2` embedding model
- [FastAPI](https://fastapi.tiangolo.com/) — modern Python web framework
- [OpenAI](https://openai.com/) — GPT-4o-mini for answer generation
