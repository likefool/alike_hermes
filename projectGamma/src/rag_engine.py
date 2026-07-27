import os
import sqlite3
import json
import math
import random
from typing import List, Dict, Any
from pathlib import Path

from openai import OpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader

# Configuration via Environment Variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
DB_PATH = os.getenv("DB_PATH", "projects/projectGamma/src/vector_store.db")
MOCK_MODE = os.getenv("MOCK_MODE", "false").lower() == "true"

class VectorStore:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_db()
        # Only initialize real client if not in mock mode
        if not MOCK_MODE:
            self.client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)
        else:
            self.client = None

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS embeddings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    metadata TEXT,
                    embedding BLOB NOT NULL
                )
            """)
            conn.commit()

    def get_embedding(self, text: str) -> List[float]:
        if MOCK_MODE:
            # Use a hash-based seed to ensure same text -> same vector in mock mode
            random.seed(abs(hash(text)) % 10**8)
            return [random.uniform(-1, 1) for _ in range(1536)]
        
        response = self.client.embeddings.create(
            input=text,
            model=EMBEDDING_MODEL
        )
        return response.data[0].embedding

    def add_documents(self, documents: List[Dict[str, Any]]):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            for doc in documents:
                embedding = self.get_embedding(doc['content'])
                # Convert list to string then bytes for storage
                embedding_str = str(embedding)
                embedding_blob = embedding_str.encode('utf-8')
                cursor.execute(
                    "INSERT INTO embeddings (content, metadata, embedding) VALUES (?, ?, ?)",
                    (doc['content'], json.dumps(doc.get('metadata', {})), embedding_blob)
                )
            conn.commit()

    def similarity_search(self, query_text: str, top_k: int = 3) -> List[Dict[str, Any]]:
        query_embedding = self.get_embedding(query_text)
        
        results = []
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT content, metadata, embedding FROM embeddings")
            rows = cursor.fetchall()
            
            for row in rows:
                content, metadata_json, embedding_blob = row
                # Decode bytes back to string then eval to list
                stored_embedding = eval(embedding_blob.decode('utf-8'))
                
                # Cosine similarity calculation
                dot_product = sum(q * s for q, s in zip(query_embedding, stored_embedding))
                norm_q = math.sqrt(sum(q**2 for q in query_embedding))
                norm_s = math.sqrt(sum(s**2 for s in stored_embedding))
                similarity = dot_product / (norm_q * norm_s) if (norm_q * norm_s) != 0 else 0
                
                results.append({
                    "content": content,
                    "metadata": json.loads(metadata_json),
                    "similarity": similarity
                })
        
        # Sort by similarity descending
        results.sort(key=lambda x: x['similarity'], reverse=True)
        return results[:top_k]

def process_file(file_path: str) -> List[Dict[str, Any]]:
    path = Path(file_path)
    text = ""
    
    if path.suffix.lower() == '.txt':
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
    elif path.suffix.lower() == '.pdf':
        reader = PdfReader(path)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    else:
        raise ValueError(f"Unsupported file type: {path.suffix}")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_text(text)
    
    return [{"content": chunk, "metadata": {"source": str(path)}} for chunk in chunks]

def main_ingest(file_paths: List[str]):
    store = VectorStore(DB_PATH)
    all_docs = []
    for fp in file_paths:
        all_docs.extend(process_file(fp))
    
    store.add_documents(all_docs)
    print(json.dumps({"status": "success", "count": len(all_docs)}, indent=2))

def main_query(query_text: str, top_k: int = 3):
    store = VectorStore(DB_PATH)
    results = store.similarity_search(query_text, top_k=top_k)
    print(json.dumps({"query": query_text, "results": results}, indent=2))

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python script.py <command> [args...]")
        sys.exit(1)
    
    cmd = sys.argv[1]
    if cmd == "ingest":
        main_ingest(sys.argv[2:])
    elif cmd == "query":
        main_query(sys.argv[2])
