import sys
sys.path.append("D:/CodeReaders")
from typing import List
from embeddings import EmbeddingsFactory
from FlagEmbedding import BGEM3FlagModel


class M3E(EmbeddingsFactory):
    def __init__(self):
        super().__init__()
        
    
    def initialize(self):
        self.embeddings = BGEM3FlagModel('BAAI/bge-m3', use_fp16=True)
    
    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        embedding = self.embeddings.encode(texts, batch_size=12, max_length=8192)['dense_vecs']
        return embedding
    

if __name__=='__main__':
    e = M3E()
    e.initialize()
    e.get_embeddings(['中国是一个伟大的国家'])