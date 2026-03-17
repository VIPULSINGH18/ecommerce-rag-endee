#!/usr/bin/env python3
"""
demo.py – ShopMind RAG demo script
Walks through ingest → search → ask against the running API.

Usage:
    python scripts/demo.py
"""

import json
import sys
import httpx

BASE = "http://localhost:8000"


def pp(data: dict):
    print(json.dumps(data, indent=2))


def section(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


def main():
    client = httpx.Client(base_url=BASE, timeout=60)

    # ── 1. Health ──────────────────────────────────────────────────────────────
    section("1. Health Check")
    r = client.get("/health")
    pp(r.json())

    # ── 2. Ingest ──────────────────────────────────────────────────────────────
    section("2. Ingesting Product Catalog into Endee")
    r = client.post("/ingest", json={"force_reingest": True})
    pp(r.json())

    # ── 3. Semantic Search (no filter) ─────────────────────────────────────────
    section("3. Semantic Search – 'noise cancelling headphones for travel'")
    r = client.post("/search", json={"query": "noise cancelling headphones for travel", "top_k": 3})
    data = r.json()
    for p in data["results"]:
        print(f"  [{p['similarity']:.3f}] {p['name']} – ${p['price']}")

    # ── 4. Filtered Search ─────────────────────────────────────────────────────
    section("4. Filtered Search – sports items under $100")
    r = client.post("/search", json={
        "query": "workout equipment for home gym",
        "top_k": 3,
        "category": "sports",
        "max_price": 100,
    })
    data = r.json()
    for p in data["results"]:
        print(f"  [{p['similarity']:.3f}] {p['name']} – ${p['price']}")

    # ── 5. RAG Q&A ─────────────────────────────────────────────────────────────
    section("5. RAG Q&A – 'What's a good gift for a coffee lover?'")
    r = client.post("/ask", json={"question": "What's a good gift for a coffee lover?"})
    data = r.json()
    print(f"\n  Q: {data['question']}")
    print(f"\n  A: {data['answer']}")
    print(f"\n  Sources: {[s['name'] for s in data['sources']]}")

    section("6. RAG Q&A – 'I need waterproof gear for hiking'")
    r = client.post("/ask", json={"question": "I need waterproof gear for hiking"})
    data = r.json()
    print(f"\n  Q: {data['question']}")
    print(f"\n  A: {data['answer']}")

    print("\n✅  Demo complete!")


if __name__ == "__main__":
    main()
