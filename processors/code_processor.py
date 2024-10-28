from typing import List, Dict
from .base import BaseProcessor
from langchain.text_splitter import RecursiveCharacterTextSplitter
from ..utils.file_utils import get_file_content
import os

class CodeProcessor(BaseProcessor):
    """代码处理器"""
    def __init__(self, chunk_size: int, chunk_overlap: int):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
    def process(self, file_paths: List[str]) -> List[Dict]:
        documents = []
        for file_path in file_paths:
            content = get_file_content(file_path)
            chunks = self.text_splitter.split_text(content)
            
            for i, chunk in enumerate(chunks):
                doc = {
                    'content': chunk,
                    'file_path': file_path,
                    'chunk_id': i,
                    'file_type': os.path.splitext(file_path)[1],
                    'relative_path': os.path.relpath(file_path)
                }
                documents.append(doc)
        return documents