import faiss
import numpy as np
import openai
import os
from sentence_transformers import SentenceTransformer

openai.api_key = os.getenv("OPENAI_API_KEY")
model = SentenceTransformer('all-MiniLM-L6-v2')

class Retriever:
    def __init__(self):
        self.index = faiss.IndexFlatL2(384)
        self.texts = []

    def add_documents(self, documents):
        vectors = model.encode(documents)
        self.index.add(np.array(vectors))
        self.texts.extend(documents)

    def query(self, query_text, top_k=3):
        query_vector = model.encode([query_text])
        D, I = self.index.search(np.array(query_vector), top_k)
        return [self.texts[i] for i in I[0]]