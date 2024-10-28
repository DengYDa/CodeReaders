from typing import List

class Config:
    DEFAULT_CHUNK_SIZE: int = 1000
    DEFAULT_CHUNK_OVERLAP: int = 200
    DEFAULT_FILE_EXTENSIONS: List[str] = ['.py', '.js', '.java', '.cpp']
    VECTOR_STORE_TYPE: str = 'faiss'
    EMBEDDINGS_TYPE: str = 'openai'