"""
RAG Engine
- Embeds product descriptions with sentence-transformers
- Stores / queries vectors in Endee vector database
- Augments LLM answers with retrieved product context
"""

import os
import json
import logging
from typing import Optional
from pathlib import Path

from endee import Endee, Precision
from sentence_transformers import SentenceTransformer
import openai

from app.catalog import load_catalog

logger = logging.getLogger(__name__)

INDEX_NAME   = "ecom_products"
EMBED_MODEL  = "all-MiniLM-L6-v2"   # 384-dim, fast & accurate
EMBED_DIM    = 384
SPACE_TYPE   = "cosine"

# Price is stored as int in [0, 999] for Endee $range filter
PRICE_SCALE  = 1   # price values already ≤ 999 in our catalog


class RAGEngine:
    def __init__(self):
        # ── Endee client ──────────────────────────────────────────────────────
        endee_url   = os.getenv("ENDEE_BASE_URL", "http://localhost:8080/api/v1")
        endee_token = os.getenv("ENDEE_AUTH_TOKEN", "")
        self.endee  = Endee(endee_token if endee_token else None)
        self.endee.set_base_url(endee_url)

        # ── Embedding model ───────────────────────────────────────────────────
        logger.info("Loading embedding model: %s", EMBED_MODEL)
        self.embedder = SentenceTransformer(EMBED_MODEL)

        # ── OpenAI client (optional – used only for /ask) ─────────────────────
        api_key = os.getenv("OPENAI_API_KEY", "")
        self.llm_available = bool(api_key)
        if self.llm_available:
            self.openai_client = openai.OpenAI(api_key=api_key)

        self._index = None

    # ── Internal helpers ──────────────────────────────────────────────────────

    def _get_index(self):
        if self._index is None:
            self._index = self.endee.get_index(name=INDEX_NAME)
        return self._index

    def _embed(self, text: str) -> list[float]:
        return self.embedder.encode(text, normalize_embeddings=True).tolist()

    # ── Public API ────────────────────────────────────────────────────────────

    def health_check(self) -> dict:
        try:
            indexes = self.endee.list_indexes()
            names   = [idx.get("name") for idx in (indexes or [])]
            return {
                "connected": True,
                "indexes": names,
                "catalog_loaded": INDEX_NAME in names,
            }
        except Exception as exc:
            return {"connected": False, "error": str(exc)}

    def ingest_products(self, force: bool = False) -> dict:
        """Embed the product catalog and upsert into Endee."""
        indexes = self.endee.list_indexes() or []
        existing = [i.get("name") for i in indexes]

        if INDEX_NAME in existing:
            if not force:
                return {
                    "status": "skipped",
                    "message": f"Index '{INDEX_NAME}' already exists. "
                               "Pass force_reingest=true to rebuild.",
                }
            self.endee.delete_index(INDEX_NAME)
            self._index = None
            logger.info("Dropped existing index '%s'.", INDEX_NAME)

        # Create index
        self.endee.create_index(
            name=INDEX_NAME,
            dimension=EMBED_DIM,
            space_type=SPACE_TYPE,
            precision=Precision.INT8,
        )
        logger.info("Created Endee index '%s'.", INDEX_NAME)

        products = load_catalog()
        index    = self._get_index()

        vectors = []
        for p in products:
            # Build a rich text chunk for embedding
            text = (
                f"{p['name']}. {p['description']} "
                f"Brand: {p['brand']}. Category: {p['category']}. "
                f"Tags: {', '.join(p.get('tags', []))}."
            )
            vec = self._embed(text)
            # price_int is used for $range filtering (Endee supports 0–999)
            price_int = min(int(p["price"]), 999)

            vectors.append({
                "id":     p["id"],
                "vector": vec,
                "meta": {
                    "name":        p["name"],
                    "description": p["description"],
                    "brand":       p["brand"],
                    "category":    p["category"],
                    "price":       p["price"],
                    "rating":      p["rating"],
                    "tags":        p.get("tags", []),
                    "image_url":   p.get("image_url", ""),
                },
                "filter": {
                    "category":  p["category"],
                    "price_int": price_int,
                },
            })

        # Upsert in batches of 50
        batch_size = 50
        for i in range(0, len(vectors), batch_size):
            index.upsert(vectors[i : i + batch_size])

        logger.info("Ingested %d products into Endee.", len(vectors))
        return {
            "status":   "success",
            "ingested": len(vectors),
            "index":    INDEX_NAME,
        }

    def semantic_search(
        self,
        query: str,
        top_k: int = 5,
        category: Optional[str] = None,
        max_price: Optional[float] = None,
    ) -> list[dict]:
        """Vector similarity search with optional metadata filters."""
        index  = self._get_index()
        vec    = self._embed(query)

        # Build Endee filter list
        filters = []
        if category:
            filters.append({"category": {"$eq": category.lower()}})
        if max_price is not None:
            price_int = min(int(max_price), 999)
            filters.append({"price_int": {"$range": [0, price_int]}})

        kwargs = dict(vector=vec, top_k=top_k, ef=128)
        if filters:
            kwargs["filter"] = filters
            kwargs["filter_boost_percentage"] = 20

        results = index.query(**kwargs)

        output = []
        for r in results:
            meta = r.get("meta", {})
            output.append({
                "id":          r.get("id"),
                "similarity":  round(r.get("similarity", 0), 4),
                "name":        meta.get("name"),
                "description": meta.get("description"),
                "brand":       meta.get("brand"),
                "category":    meta.get("category"),
                "price":       meta.get("price"),
                "rating":      meta.get("rating"),
                "tags":        meta.get("tags", []),
            })
        return output

    def ask(self, question: str, top_k: int = 4) -> dict:
        """
        RAG pipeline:
          1. Retrieve top-k relevant products from Endee.
          2. Build a prompt with product context.
          3. Generate an answer with GPT-4o-mini (or fallback if no API key).
        """
        # Step 1 – Retrieve
        products = self.semantic_search(query=question, top_k=top_k)

        if not products:
            return {
                "question": question,
                "answer":   "No relevant products found in the catalog.",
                "sources":  [],
            }

        # Step 2 – Build context
        context_parts = []
        for i, p in enumerate(products, 1):
            context_parts.append(
                f"[Product {i}] {p['name']} by {p['brand']}\n"
                f"  Category: {p['category']} | Price: ${p['price']} | Rating: {p['rating']}/5\n"
                f"  Description: {p['description']}"
            )
        context = "\n\n".join(context_parts)

        system_prompt = (
            "You are ShopMind, an expert e-commerce assistant. "
            "Use ONLY the product information provided below to answer the customer's question. "
            "Be helpful, concise, and specific. If the answer cannot be found in the products, "
            "say so politely and suggest the customer browse related categories."
        )
        user_prompt = (
            f"Customer question: {question}\n\n"
            f"Available products:\n{context}\n\n"
            "Please answer the customer's question based on the products above."
        )

        # Step 3 – Generate
        if self.llm_available:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user",   "content": user_prompt},
                ],
                max_tokens=500,
                temperature=0.3,
            )
            answer = response.choices[0].message.content.strip()
        else:
            # Fallback: structured summary when no LLM key is set
            lines = [
                f"Here are the top {len(products)} products matching your question:\n"
            ]
            for p in products:
                lines.append(
                    f"• **{p['name']}** by {p['brand']} – ${p['price']} "
                    f"(Rating: {p['rating']}/5)\n  {p['description']}"
                )
            lines.append(
                "\n_Tip: Set OPENAI_API_KEY in your .env to enable "
                "fully generated natural-language answers._"
            )
            answer = "\n".join(lines)

        return {
            "question": question,
            "answer":   answer,
            "sources":  [{"id": p["id"], "name": p["name"]} for p in products],
        }
