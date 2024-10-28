from typing import List
from .base import BaseComponent
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceEmbeddings
from FlagEmbedding import BGEM3FlagModel

class EmbeddingsFactory(BaseComponent):
    """嵌入向量模型工厂类"""
    def __init__(self):
        self.embeddings = None
        
    def initialize(self, embeddings_type: str = 'huggingface', **kwargs):
        if embeddings_type == 'openai':
            self.embeddings = OpenAIEmbeddings(**kwargs)
        elif embeddings_type == 'huggingface':
            self.embeddings = HuggingFaceEmbeddings(**kwargs)
        else:
            raise ValueError(f"Unsupported embeddings type: {embeddings_type}")

    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        return self.embeddings.embed_documents(texts)