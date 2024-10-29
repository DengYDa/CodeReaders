from typing import List, Dict
from .base import BaseComponent
from langchain.vectorstores import FAISS, Chroma
import os
import json

class VectorStoreManager(BaseComponent):
    """向量存储管理类"""
    def __init__(self):
        self.vector_store = None
        self.store_type = None
        
    def initialize(self, store_type: str = 'faiss', **kwargs):
        self.store_type = store_type
        
    def create_store(self, texts: List[str], embeddings, metadatas: List[Dict] = None):
        if self.store_type == 'faiss':
            self.vector_store = FAISS.from_texts(texts=texts, embedding=embeddings, metadatas=metadatas)
        elif self.store_type == 'chroma':
            self.vector_store = Chroma.from_texts(texts=texts, embedding=embeddings, metadatas=metadatas)
            
    def save(self, path: str):
        os.makedirs(path, exist_ok=True)
        if self.store_type == 'faiss':
            self.vector_store.save_local(path)
        
    def load(self, path: str, embeddings):
        if self.store_type == 'faiss':
            self.vector_store = FAISS.load_local(path, embeddings)
            
    def search(self, query: str, k: int = 5) -> List[Dict]:
        results = self.vector_store.similarity_search_with_score(query, k=k)
        return [{
            'content': doc.page_content,
            'metadata': doc.metadata,
            'similarity_score': float(score)
        } for doc, score in results]