import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np

from genai.gemini_client import embed
from scraper.mongo_client import get_db

import time

from google.genai.errors import ClientError

def cosine_similarity(a, b):
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def embed_all_news():
    db = get_db()
    collection = db.raw_news

    articles = list(collection.find({"embedding": {"$exists": False}}))
    print(f"Embedding {len(articles)} articles without an existing embedding...")

    i = 0
    while i < len(articles):
        article = articles[i]
        text = f"{article.get('headline', '')}. {article.get('summary', '')}"
        try:
            vector = embed(text)
            collection.update_one({"_id": article["_id"]}, {"$set": {"embedding": vector}})
            i += 1
            if i % 20 == 0:
                print(f"  ...{i}/{len(articles)} done")
        except ClientError as e:
            if "RESOURCE_EXHAUSTED" in str(e):
                print(f"  Rate limited at article {i}/{len(articles)} — waiting 30s...")
                time.sleep(30)
                # don't increment i — retry the same article
            else:
                raise

    print("Done embedding all articles.")

def retrieve_relevant_articles(question: str, top_k: int = 3):
    query_vector = embed(question)

    db = get_db()
    articles = list(db.raw_news.find({"embedding": {"$exists": True}}))

    scored = []
    for article in articles:
        score = cosine_similarity(query_vector, article["embedding"])
        scored.append((score, article))

    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:top_k]


def rag_answer(question: str, top_k: int = 3) -> str:
    from genai.gemini_client import ask

    top_articles = retrieve_relevant_articles(question, top_k=top_k)

    context = "\n\n".join(
        f"[{score:.3f}] {a.get('headline', '')}: {a.get('summary', '')}"
        for score, a in top_articles
    )

    prompt = f"""
Answer the question using ONLY the news context below. If the context
doesn't contain enough information to answer, say so honestly rather
than guessing.

Context:
{context}

Question: {question}

Answer:
"""
    return ask(prompt)